from mvr_api import CompiledPack, EvidenceItem, FirstCallRequest


evidence: EvidenceItem = {
    "id": "EV-1",
    "evidence_type": "survey",
    "evidence_origin": "field_research",
    "source_grade": "B",
    "entity_archetype": "retail_chain",
    "evidence_geography": {"country": "UG", "city": "Kampala"},
    "structured_values": {"trust": 72.0, "permission": 68.0},
}

compiled_pack: CompiledPack = {"survey_pack": [evidence]}
first_call: FirstCallRequest = {
    "subject": {"entity_name": "Example venture", "entity_archetype": "fintech_lending"},
    "market_scope": {"country": "UG", "sector": "supplier finance"},
}

bad_evidence_type: EvidenceItem = {"evidence_type": "blog_post"}  # type: ignore
bad_archetype: FirstCallRequest = {"entity_archetype": "generic_startup"}  # type: ignore
bad_compiled_pack: CompiledPack = {"unexpected_pack": []}  # type: ignore

_ = (compiled_pack, first_call, bad_evidence_type, bad_archetype, bad_compiled_pack)
