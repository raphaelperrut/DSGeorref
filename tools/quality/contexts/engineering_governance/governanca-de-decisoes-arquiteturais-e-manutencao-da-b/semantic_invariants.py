from __future__ import annotations

from collections.abc import Callable
from typing import Any

from validation_types import Finding


def _portfolio(snapshot: dict[str, Any], artifact: str) -> list[Finding]:
    rows = snapshot["reconciliations"]
    stable_ids = [row["stable_id"] for row in rows]
    github_ids = [
        (
            row["github_issue"]["repository"],
            row["github_issue"]["issue_number"],
            row["github_issue"]["node_id"],
        )
        for row in rows
    ]
    findings: list[Finding] = []
    if len(stable_ids) != len(set(stable_ids)) or len(github_ids) != len(
        set(github_ids)
    ):
        findings.append(
            Finding(
                artifact,
                "INCONSISTENT_RECONCILIATION",
                "stable and GitHub identities must be one-to-one",
            )
        )
    if any(row["stable_id"] != row["repository_issue"]["issue_id"] for row in rows):
        findings.append(
            Finding(
                artifact,
                "INCONSISTENT_RECONCILIATION",
                "stable_id must equal repository_issue.issue_id",
            )
        )
    summary = snapshot["reconciliation_summary"]
    if summary["reconciled"] != len(rows) or summary["unresolved"] != 0:
        findings.append(
            Finding(
                artifact,
                "INCONSISTENT_RECONCILIATION",
                "summary must report every row reconciled and zero unresolved",
            )
        )
    return findings


def _forecast(forecast: dict[str, Any], artifact: str) -> list[Finding]:
    findings: list[Finding] = []
    interval = forecast["interval"]
    if not interval["minimum"] <= interval["mode"] <= interval["maximum"]:
        findings.append(
            Finding(
                artifact,
                "INVALID_INTERVAL_ORDER",
                "minimum <= mode <= maximum is required",
            )
        )
    snapshot, variance = forecast["snapshot"], forecast["variance"]
    if (
        variance["basis_snapshot_id"] != snapshot["snapshot_id"]
        or variance["basis_snapshot_version"] != snapshot["snapshot_version"]
    ):
        findings.append(
            Finding(
                artifact,
                "SNAPSHOT_VARIANCE_MISMATCH",
                "variance must reference the declared snapshot id and version",
            )
        )
    return findings


def _boundaries(decision: dict[str, Any], artifact: str) -> list[Finding]:
    boundaries = decision["boundaries"]
    ids = [boundary["boundary_id"] for boundary in boundaries.values()]
    concerns = [boundary["concern"] for boundary in boundaries.values()]
    findings: list[Finding] = []
    distinct = set(boundaries) == {"core", "api", "runners"}
    if not distinct or len(set(ids)) != 3 or len(set(concerns)) != 3:
        findings.append(
            Finding(
                artifact,
                "BOUNDARY_COLLAPSED",
                "core, api and runners must have distinct ids and concerns",
            )
        )
    if any(boundary["runtime_materialized"] is not False for boundary in boundaries.values()):
        findings.append(
            Finding(
                artifact,
                "RUNTIME_MATERIALIZATION_ATTEMPTED",
                "all boundaries must remain declarative",
            )
        )
    return findings


def validate_semantics(
    examples: dict[str, dict[str, Any]], example_paths: dict[str, str]
) -> list[Finding]:
    rules: dict[str, Callable[[dict[str, Any], str], list[Finding]]] = {
        "portfolio-snapshot": _portfolio,
        "issue-forecast": _forecast,
        "foundation-boundaries": _boundaries,
    }
    findings: list[Finding] = []
    for contract_id, example in sorted(examples.items()):
        findings.extend(rules[contract_id](example, example_paths[contract_id]))
    return findings
