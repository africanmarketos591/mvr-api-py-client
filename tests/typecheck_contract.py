from mvr_api import CompiledPack, EvidenceItem, FirstCallRequest, RecommendedInputsRequest


evidence: EvidenceItem = {
    "id": "EV-1",
    "evidence_type": "survey",
    "evidence_origin": "field_research",
    "source_grade": "B",
    "source_class": "structured_field_research",
    "stakeholder_class": "retailer",
    "collection_method": "structured_interview_protocol",
    "entity_archetype": "retail_chain",
    "guardian_tier": "meso_community",
    "source_confidence": "high",
    "review_status": "verified",
    "privacy_envelope": {"contains_pii": False},
    "source_artifacts": [{"artifact_id": "ART-1", "human_reviewed": True}],
    "evidence_geography": {"country": "UG", "city": "Kampala"},
    "structured_values": {"trust": 72.0, "permission": 68.0},
}

compiled_pack: CompiledPack = {"survey_pack": [evidence]}
first_call: FirstCallRequest = {
    "subject": {"entity_name": "Example venture", "entity_archetype": "generic_startup", "custom_discovery_hint": "early"},
    "entity_archetype": "generic_startup",
    "market_scope": {"country": "UG", "sector": "supplier finance"},
}
recommended_inputs: RecommendedInputsRequest = {"endpoint": "/v1/decision-check", "entity_archetype": "fintech_lending"}

bad_evidence_type: EvidenceItem = {"evidence_type": "blog_post"}  # type: ignore
bad_recommended_archetype: RecommendedInputsRequest = {"entity_archetype": "generic_startup"}  # type: ignore
bad_source_class: EvidenceItem = {"source_class": "blog"}  # type: ignore
bad_stakeholder_class: EvidenceItem = {"stakeholder_class": "random_person"}  # type: ignore
bad_collection_method: EvidenceItem = {"collection_method": "scraped_guess"}  # type: ignore
bad_compiled_pack: CompiledPack = {"unexpected_pack": []}  # type: ignore

_ = (compiled_pack, first_call, recommended_inputs, bad_evidence_type, bad_recommended_archetype, bad_source_class, bad_stakeholder_class, bad_collection_method, bad_compiled_pack)
