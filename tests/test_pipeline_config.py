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
