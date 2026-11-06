"""Conformance of the instance policy against the existing BC-002 freeze."""

import json
import runpy
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
FREEZE = HERE.parent / "contas-locais-bootstrap-unico-sessoes-tokens-e-adapter"
POLICY = json.loads((HERE / "policy.json").read_text(encoding="utf-8"))
CONTRACT = json.loads((FREEZE / "contract.json").read_text(encoding="utf-8"))
RULES = runpy.run_path(str(FREEZE / "conformance.py"))


def test_epic_009_politica() -> None:
    assert POLICY["default_decision"] == "deny"
    assert POLICY["project_roles"] == CONTRACT["policies"]["authorization"]["roles"]
    assert POLICY["role_grant_rule"] == "explicit_grant_for_current_membership"
    assert POLICY["instance_grant_rule"] == "explicit_grant_for_account"
    operations = POLICY["operations"]
    assert set(operations) == set(CONTRACT["operations"])
    assert {key: row["grant_source"] for key, row in operations.items()} == {
        "post_auth_bootstrap": "installation_capability",
        "post_auth_session": "authentication_policy",
        "get_auth_oidc_callback": "authentication_policy",
        "delete_auth_session": "central_policy",
        "post_auth_tokens": "central_policy",
        "get_projects_projectid_members": "project_membership",
        "post_projects_projectid_members": "project_membership",
        "get_authorization_check": "central_policy",
    }
    for key, row in operations.items():
        frozen = CONTRACT["operations"][key]
        assert row["permission"] == frozen["permission"]
        facts = dict.fromkeys((guard["fact"] for guard in frozen["guards"]), True)
        for guard in frozen["guards"]:
            missing = facts.copy()
            del missing[guard["fact"]]
            denied = RULES["decide_operation"](CONTRACT, key, missing)
            assert denied["allowed"] is False
            assert denied["effects"] == []
            rejected = RULES["decide_operation"](CONTRACT, key, facts | {guard["fact"]: False})
            assert rejected["code"] == guard["error"]
            assert rejected["status"] == frozen["errors"][guard["error"]]
            assert rejected["effects"] == []

    assert POLICY["account_machine"] == "account"
    machine = CONTRACT["machines"]["account"]
    assert set(machine["states"]) == {"absent", "active", "inactive", "locked"}
    assert {(edge["from"], edge["event"], edge["to"]) for edge in machine["transitions"]} == {
        ("absent", "create", "active"),
        ("active", "deactivate", "inactive"),
        ("locked", "deactivate", "inactive"),
        ("inactive", "activate", "active"),
        ("active", "lock", "locked"),
        ("locked", "unlock", "active"),
    }
    for edge in machine["transitions"]:
        facts = dict.fromkeys(edge["requires"], True)
        step = (CONTRACT, "account", edge["from"], edge["event"])
        assert RULES["next_state"](*step, facts) == edge["to"]
        for guard in edge["requires"]:
            with pytest.raises(RULES["ContractViolation"]):
                RULES["next_state"](*step, facts | {guard: False})


def test_req_auth_impl_007() -> None:
    throttle = POLICY["throttling"]
    assert throttle["requirement"] == CONTRACT["requirement"] == "REQ-AUTH-IMPL-007"
    assert throttle["evidence"] == CONTRACT["policies"]["throttling"]["evidence_schema"]
    assert throttle["machine"] == "throttle"
    assert throttle["eligible_states"] == ["open"]
    assert set(CONTRACT["machines"]["throttle"]["states"]) == {"open", "limited", "locked"}
    examples = json.loads((FREEZE / "examples.json").read_text(encoding="utf-8"))
    boundary = json.loads((FREEZE / "boundary-evidence.schema.json").read_text(encoding="utf-8"))
    observations = examples["throttle_observations"]
    assert observations
    for observation in observations:
        RULES["validate_boundary"](observation, boundary, throttle["machine"])
