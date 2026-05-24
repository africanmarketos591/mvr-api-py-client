from mvr_api import MVRClient


client = MVRClient()

resolved = client.entity_resolve("MTN Nigeria", country="NG")
print("resolved:", resolved.get("canonical_name"))

evidence = client.evidence_completeness(
    {
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
    }
)
print("evidence status:", evidence.get("status"))
print("sandbox:", evidence.get("response_meta", {}).get("environment") == "sandbox")
