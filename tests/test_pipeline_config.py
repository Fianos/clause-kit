import pytest
from src.pipeline import DOMAIN_META
from src.ingest import ALLOWLISTS
from src.extract import DOMAIN_FACT_SCHEMAS, DOMAIN_PROVISION_URI_GUIDANCE


def test_privacy_apps_domain_meta_present():
    assert "privacy-apps" in DOMAIN_META
    assert DOMAIN_META["privacy-apps"]["source_type"] == "akn"
    assert DOMAIN_META["privacy-apps"]["chunk_strategy"] == "schedule_clause"
    assert "privacy-act-1988.xml" in DOMAIN_META["privacy-apps"]["corpus_filename"]


def test_privacy_apps_allowlist_has_13_entries():
    allowed = ALLOWLISTS["privacy-apps"]
    assert len(allowed) == 13
    assert "app-1" in allowed
    assert "app-13" in allowed
    assert "app-14" not in allowed


def test_privacy_apps_fact_schema_present():
    schema = DOMAIN_FACT_SCHEMAS["privacy-apps"]
    assert "entity_type" in schema
    assert "consent_given" in schema
    assert "cross_border_disclosure" in schema


def test_privacy_apps_provision_uri_guidance_present():
    guidance = DOMAIN_PROVISION_URI_GUIDANCE["privacy-apps"]
    assert "/akn/au/act/1988/119/schedule/1/clause/" in guidance


def test_ssa_bereavement_domain_meta_present():
    assert "ssa-bereavement" in DOMAIN_META
    assert DOMAIN_META["ssa-bereavement"]["source_type"] == "akn"
    assert DOMAIN_META["ssa-bereavement"]["definitions_section_num"] == "21"


def test_sis_death_benefits_domain_meta_present():
    assert "sis-death-benefits" in DOMAIN_META
    assert DOMAIN_META["sis-death-benefits"]["source_type"] == "akn"


def test_ssa_bereavement_allowlist_contains_key_sections():
    allowed = ALLOWLISTS["ssa-bereavement"]
    assert "21" in allowed
    assert "82" in allowed
    assert "83" in allowed
    assert "146g" in allowed
    assert "514a" in allowed
    assert "1065" not in allowed


def test_ssa_bereavement_fact_schema_present():
    schema = DOMAIN_FACT_SCHEMAS["ssa-bereavement"]
    assert "payment_type" in schema
    assert "relationship_to_deceased" in schema
    assert "claimant_notified_centrelink" in schema


def test_ssa_bereavement_provision_uri_guidance_present():
    guidance = DOMAIN_PROVISION_URI_GUIDANCE["ssa-bereavement"]
    assert "/akn/au/act/1991/46/section/" in guidance


def test_sis_death_benefits_allowlist_contains_key_sections():
    allowed = ALLOWLISTS["sis-death-benefits"]
    assert "55a" in allowed
    assert "68aa" in allowed
    assert "68a" not in allowed  # trustee conduct, not death benefits
    assert "51" not in allowed


def test_sis_death_benefits_fact_schema_present():
    schema = DOMAIN_FACT_SCHEMAS["sis-death-benefits"]
    assert "member_status" in schema
    assert "death_benefit_nomination" in schema
    assert "beneficiary_type" in schema


def test_sis_death_benefits_provision_uri_guidance_present():
    guidance = DOMAIN_PROVISION_URI_GUIDANCE["sis-death-benefits"]
    assert "/akn/au/act/1993/78/section/" in guidance
