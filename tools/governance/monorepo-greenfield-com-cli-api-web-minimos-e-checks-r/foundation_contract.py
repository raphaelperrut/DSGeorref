from __future__ import annotations


EXPECTED_SURFACES = [
    {
        "surface": "CLI",
        "invocation": "APPLICATION_SERVICE_PORT",
        "contract_source": "monorepo-foundation-contract",
    },
    {
        "surface": "HTTP_API",
        "invocation": "APPLICATION_SERVICE_PORT",
        "contract_source": "contracts/http/openapi.yaml",
    },
    {
        "surface": "WEB",
        "invocation": "HTTP_API_OPENAPI_CLIENT",
        "contract_source": "contracts/http/openapi.yaml",
    },
]

EXPECTED_FAILURE_POLICY = {
    "mode": "FAIL_CLOSED",
    "silent_fallback": False,
    "publication_on_error": "PROHIBITED",
    "error_states": [
        "SEMANTIC_MAPPING_MISSING",
        "CONTRACT_VERSION_UNSUPPORTED",
        "AUTHORITY_VIOLATION",
    ],
}
