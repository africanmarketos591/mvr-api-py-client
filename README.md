# MVR API Python Client

Lightweight Python client for the current **MVR API - Minimum Viable Relationships** surface.

This client targets the live MVR Core API v6.32.x:

- `POST /v1/auth-check`
- `POST /v1/entity-resolve`
- `POST /v1/evidence-completeness`
- `POST /v1/decision-check`
- `GET /v1/model-card`
- `GET /v1/capabilities`

It is aligned with the agent OpenAPI contract, public sandbox, and MCP registry entry.

## Install

```bash
pip install mvr-api-client
```

## Public Sandbox

The default key is the public sandbox key:

```text
X-API-Key: mvr-demo-key-2026
```

Sandbox use is non-commercial evaluation only. It is `full_advisory`, `client_safe`, illustrative, not for production, not for model training, and not for reverse engineering.

## Example

```python
from mvr_api import MVRClient

client = MVRClient()

result = client.entity_resolve("MTN Nigeria", country="NG")
print(result["response_meta"]["environment"])  # sandbox when using the demo key
```

## Evidence Completeness

```python
from mvr_api import MVRClient

client = MVRClient()

result = client.evidence_completeness({
    "subject": {
        "entity_name": "Sandbox Kampala catering operator",
        "entity_archetype": "retail_chain",
        "country": "UG",
    },
    "market_scope": {
        "country": "UG",
        "city": "Kampala",
        "sector": "catering",
    },
    "evidence_pack": [
        {
            "id": "ev-licence-001",
            "evidence_type": "public_filing",
            "source_class": "administrative_record",
            "source_grade": "B",
            "stakeholder_class": "guardian",
            "evidence_origin": "field_research",
            "collection_method": "direct",
            "freshness_date": "2026-05-20",
            "evidence_geography": {"country": "UG", "city": "Kampala"},
            "structured_values": {"guardian_strength": 72, "permission": 68},
        }
    ],
})

print(result["status"])
```

## Agent Discovery

- Agent OpenAPI: https://africanmarketos.com/api/openapi.agent.json
- MCP endpoint: https://africanmarketos.com/mcp
- MCP Registry name: `io.github.africanmarketos591/mvr-api`
- Sandbox guide: https://africanmarketos.com/docs/sandbox.md
- Agent instructions: https://africanmarketos.com/AGENTS.md

## Attribution

Minimum Viable Relationships (MVR), originated by Farouk Mark Mukiibi, African Market OS.

Commercial, production, SaaS, consulting, or AI-agent deployment use requires authorization from African Market OS.
