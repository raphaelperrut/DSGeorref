"""Reuse the integrated composition and disposable PostgreSQL fixtures."""

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
source = ROOT / "tests/backend/identity_access/resource_authorization/conftest.py"
spec = importlib.util.spec_from_file_location("security_resource_fixtures", source)
upstream = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = upstream
spec.loader.exec_module(upstream)

database = upstream.database
runtime = upstream.runtime
authorization = upstream.authorization
ADAPTER, CONTRACT = upstream.ADAPTER, upstream.CONTRACT
