from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import re
import subprocess
from pathlib import Path
from typing import Any

SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")


def _scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def _locked_versions(path: Path) -> dict[str, str]:
    sections = {"runtime", "native_stack", "python_stack"}
    current: str | None = None
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if not raw_line or raw_line.lstrip().startswith("#"):
            continue
        if not raw_line.startswith(" ") and raw_line.endswith(":"):
            current = raw_line[:-1] if raw_line[:-1] in sections else None
            continue
        if current and raw_line.startswith("  ") and not raw_line.startswith("    "):
            key, separator, value = raw_line.strip().partition(":")
            if separator:
                values[f"{current}.{key}"] = _scalar(value)
    required = {
        "runtime.python",
        "native_stack.gdal",
        "native_stack.proj",
        "native_stack.geos",
        "native_stack.rasterio",
        "native_stack.shapely",
        "native_stack.postgresql",
        "native_stack.postgis",
        "python_stack.fastapi",
        "python_stack.pydantic",
        "python_stack.celery",
    }
    missing = sorted(required - values.keys())
    if missing:
        raise RuntimeError(f"source lock is missing required versions: {missing}")
    return values


def _require_equal(name: str, actual: str, expected: str) -> None:
    if actual != expected:
        raise RuntimeError(f"{name} version mismatch: expected {expected}, got {actual}")


def _runtime_checks(locked: dict[str, str]) -> dict[str, Any]:
    import celery
    import fastapi
    import numpy
    import pydantic
    import rasterio
    import shapely
    from osgeo import gdal, osr
    from rasterio.io import MemoryFile
    from rasterio.transform import from_origin
    from rasterio.warp import transform
    from shapely.geometry import Point, Polygon

    versions = {
        "python": platform.python_version(),
        "gdal": gdal.VersionInfo("RELEASE_NAME"),
        "proj": rasterio.__proj_version__,
        "geos": shapely.geos_version_string,
        "rasterio": rasterio.__version__,
        "shapely": shapely.__version__,
        "fastapi": fastapi.__version__,
        "pydantic": pydantic.__version__,
        "celery": celery.__version__,
    }
    for name in versions:
        section = (
            "runtime"
            if name == "python"
            else "native_stack"
            if name
            in {
                "gdal",
                "proj",
                "geos",
                "rasterio",
                "shapely",
            }
            else "python_stack"
        )
        _require_equal(name, versions[name], locked[f"{section}.{name}"])

    proj_version_output = subprocess.run(
        ["proj"], input="", text=True, capture_output=True, check=False
    ).stderr
    if locked["native_stack.proj"] not in proj_version_output:
        raise RuntimeError("PROJ CLI and Rasterio do not expose the locked PROJ version")

    source_crs = osr.SpatialReference()
    target_crs = osr.SpatialReference()
    source_crs.ImportFromEPSG(4326)
    target_crs.ImportFromEPSG(3857)
    projected = osr.CoordinateTransformation(source_crs, target_crs).TransformPoint(-46.63, -23.55)
    if not all(math.isfinite(value) for value in projected[:2]):
        raise RuntimeError("GDAL/PROJ coordinate transformation returned non-finite values")

    xs, ys = transform("EPSG:4326", "EPSG:3857", [-46.63], [-23.55])
    if not math.isfinite(xs[0]) or not math.isfinite(ys[0]):
        raise RuntimeError("Rasterio/GDAL/PROJ transform failed")

    raster = numpy.arange(4, dtype="uint8").reshape((1, 2, 2))
    with MemoryFile() as memory:
        with memory.open(
            driver="GTiff",
            height=2,
            width=2,
            count=1,
            dtype="uint8",
            crs="EPSG:4326",
            transform=from_origin(-47.0, -23.0, 0.1, 0.1),
        ) as dataset:
            dataset.write(raster)
        with memory.open() as dataset:
            if not numpy.array_equal(dataset.read(), raster):
                raise RuntimeError("Rasterio/GDAL in-memory GeoTIFF round trip failed")

    polygon = Polygon([(0, 0), (2, 0), (2, 2), (0, 2)])
    if (
        not polygon.is_valid
        or not polygon.contains(Point(1, 1))
        or polygon.buffer(1).area <= polygon.area
    ):
        raise RuntimeError("Shapely/GEOS topology operation failed")

    return {
        "versions": versions,
        "checks": [
            "gdal_proj_coordinate_transform",
            "rasterio_gdal_geotiff_round_trip",
            "shapely_geos_topology",
        ],
    }


def _database_checks(dsn: str, locked: dict[str, str]) -> dict[str, Any]:
    import psycopg

    with psycopg.connect(dsn, autocommit=False) as connection:
        with connection.cursor() as cursor:
            cursor.execute("CREATE EXTENSION IF NOT EXISTS postgis")
            cursor.execute(
                "SELECT current_setting('server_version'), current_setting('server_version_num'), "
                "postgis_lib_version()"
            )
            postgresql_version, postgresql_version_num, postgis_version = cursor.fetchone()
            postgresql_major, postgresql_patch = (
                int(part) for part in locked["native_stack.postgresql"].split(".")
            )
            expected_postgresql_num = f"{postgresql_major * 10000 + postgresql_patch:06d}"
            if postgresql_version_num != expected_postgresql_num:
                raise RuntimeError(
                    f"PostgreSQL version mismatch: expected {locked['native_stack.postgresql']}, "
                    f"got {postgresql_version} ({postgresql_version_num})"
                )
            _require_equal("PostGIS", postgis_version, locked["native_stack.postgis"])
            cursor.execute(
                "SELECT ST_SRID(ST_Transform(ST_SetSRID(ST_Point(-46.63, -23.55), 4326), 3857)), "
                "ST_Intersects(ST_Buffer(ST_SetSRID(ST_Point(0, 0), 4326)::geography, 1000), "
                "ST_SetSRID(ST_Point(0.001, 0.001), 4326)::geography)"
            )
            srid, intersects = cursor.fetchone()
            if srid != 3857 or intersects is not True:
                raise RuntimeError("PostGIS transform/topology compatibility check failed")
        connection.rollback()
    return {
        "versions": {"postgresql": postgresql_version, "postgis": postgis_version},
        "checks": ["postgis_extension_load", "postgis_transform", "postgis_geography_topology"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Fail-closed native stack ABI smoke")
    parser.add_argument("--source-lock", type=Path, required=True)
    parser.add_argument("--candidate-image-digest", required=True)
    parser.add_argument("--postgres-dsn", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    if not SHA256_RE.fullmatch(args.candidate_image_digest):
        raise RuntimeError("candidate image digest must be an immutable sha256 digest")
    source_bytes = args.source_lock.read_bytes()
    locked = _locked_versions(args.source_lock)
    report = {
        "schema_version": "1.0.0",
        "result": "PASS",
        "candidate_image_digest": args.candidate_image_digest,
        "source_lock_digest": f"sha256:{hashlib.sha256(source_bytes).hexdigest()}",
        "runtime": _runtime_checks(locked),
        "database": _database_checks(args.postgres_dsn, locked),
        "components_verified": [
            "Python",
            "GDAL",
            "PROJ",
            "GEOS",
            "Rasterio",
            "Shapely",
            "PostgreSQL",
            "PostGIS",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
