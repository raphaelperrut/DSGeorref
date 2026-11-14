"""Canonical identity requirements exercised with the unchanged approved runtime."""

import importlib.util
from pathlib import Path

LEGACY = Path(__file__).resolve().parents[1] / "local_identity/test_requirements.py"
spec = importlib.util.spec_from_file_location("resource_identity_requirements", LEGACY)
upstream = importlib.util.module_from_spec(spec)
spec.loader.exec_module(upstream)

# Reuse the canonical behavioral assertions, including failures and persisted effects.
test_req_auth_impl_001 = upstream.test_req_auth_impl_001
test_req_auth_impl_002 = upstream.test_req_auth_impl_002
test_req_auth_impl_003 = upstream.test_req_auth_impl_003
test_req_auth_impl_004 = upstream.test_req_auth_impl_004
test_req_auth_impl_005 = upstream.test_req_auth_impl_005
test_req_auth_impl_006 = upstream.test_req_auth_impl_006
test_req_auth_impl_008 = upstream.test_req_auth_impl_008
test_req_auth_impl_009 = upstream.test_req_auth_impl_009
test_req_auth_impl_0010 = upstream.test_req_auth_impl_0010
