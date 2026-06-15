import pytest
from src.schema import Docref, Rule, DomainFile, EuAiActFacts, NdbFacts, Scenario, RuleResult


def test_rule_high_codifiability():
    r = Rule(
        rule_id="eu-annex-iii-1a",
        label="Real-time biometric identification",
        condition={"and": [{"==": [{"var": "real_time_biometric"}, True]}, {"==": [{"var": "publicly_accessible_spaces"}, True]}]},
        obligation="Prohibited under Article 5(1)(h)",
        scope="Providers and deployers",
        exceptions=["Victim search"],
        codifiability="high",
        docref=Docref(source_doc="EU AI Act", article="Article 5", section="1(h)", url="https://eur-lex.europa.eu/...")
    )
    assert r.codifiability == "high"
    assert r.condition is not None


def test_rule_low_codifiability_has_null_condition():
    r = Rule(
        rule_id="eu-5-1-b",
        label="Manipulation of vulnerable groups",
        condition=None,
        obligation="Prohibited subliminal manipulation exploiting vulnerabilities",
        scope="Providers",
        exceptions=[],
        codifiability="low",
        docref=Docref(source_doc="EU AI Act", article="Article 5", section="1(b)", url="https://eur-lex.europa.eu/...")
    )
    assert r.condition is None


def test_eu_ai_act_facts_valid():
    facts = EuAiActFacts(
        system_name="HR Screener",
        deployment_sector="employment",
        publicly_accessible_spaces=False,
        involves_safety_component=False,
        is_gpai_model=False,
        real_time_biometric=False,
        post_hoc_biometric=False,
        art6_3_exception_narrow_procedure=False,
        art6_3_exception_human_override=False,
        art6_3_exception_preparatory_task=False,
        art6_3_exception_contravention_check=False,
    )
    assert facts.deployment_sector == "employment"


def test_ndb_facts_valid():
    facts = NdbFacts(
        incident_type="unauthorised_access",
        data_categories=["health", "financial"],
        encryption_status="unencrypted",
        individuals_affected="1000+",
        likely_recipient="criminal",
        individual_vulnerability="health_patients",
    )
    assert "health" in facts.data_categories


def test_domain_file_roundtrip(tmp_path):
    import json
    df = DomainFile(
        domain="eu-ai-act",
        version="Regulation (EU) 2024/1689",
        extracted_at="2026-06-14",
        source_url="https://eur-lex.europa.eu/...",
        rules=[],
        scenarios=[],
    )
    path = tmp_path / "test.json"
    path.write_text(df.model_dump_json(indent=2))
    loaded = DomainFile.model_validate_json(path.read_text())
    assert loaded.domain == "eu-ai-act"


def test_rule_result_null_for_low_codifiability():
    rr = RuleResult(
        rule_id="x",
        matched=None,
        codifiability="low",
        label="Test",
        obligation="...",
        docref=Docref(source_doc="", article="", section="", url="")
    )
    assert rr.matched is None
