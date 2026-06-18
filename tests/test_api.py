import pytest
from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)

EU_FACTS_FACIAL = {
    "system_name": "FaceID Pro",
    "deployment_sector": "law_enforcement",
    "publicly_accessible_spaces": True,
    "involves_safety_component": False,
    "is_gpai_model": False,
    "real_time_biometric": True,
    "post_hoc_biometric": False,
    "art6_3_exception_narrow_procedure": False,
    "art6_3_exception_human_override": False,
    "art6_3_exception_preparatory_task": False,
    "art6_3_exception_contravention_check": False,
}

EU_FACTS_CHATBOT = {
    "system_name": "SupportBot",
    "deployment_sector": "general",
    "publicly_accessible_spaces": False,
    "involves_safety_component": False,
    "is_gpai_model": False,
    "real_time_biometric": False,
    "post_hoc_biometric": False,
    "art6_3_exception_narrow_procedure": False,
    "art6_3_exception_human_override": False,
    "art6_3_exception_preparatory_task": False,
    "art6_3_exception_contravention_check": False,
}


def test_list_domains():
    r = client.get("/domains")
    assert r.status_code == 200
    domains = r.json()
    assert "eu-ai-act" in domains
    assert "ndb" in domains


def test_get_rules_eu():
    r = client.get("/domains/eu-ai-act/rules")
    assert r.status_code == 200
    data = r.json()
    assert data["domain"] == "eu-ai-act"
    assert len(data["rules"]) == 32


def test_get_rules_ndb():
    r = client.get("/domains/ndb/rules")
    assert r.status_code == 200
    data = r.json()
    assert data["domain"] == "ndb"
    assert len(data["rules"]) == 54


def test_get_scenarios_eu():
    r = client.get("/domains/eu-ai-act/scenarios")
    assert r.status_code == 200
    scenarios = r.json()
    assert len(scenarios) == 5
    ids = [s["id"] for s in scenarios]
    assert "facial-recognition-public" in ids


def test_get_scenarios_ndb():
    r = client.get("/domains/ndb/scenarios")
    assert r.status_code == 200
    scenarios = r.json()
    assert len(scenarios) == 4


def test_evaluate_eu_facial_recognition_has_matches():
    r = client.post("/domains/eu-ai-act/evaluate", json=EU_FACTS_FACIAL)
    assert r.status_code == 200
    results = r.json()
    assert len(results) == 32
    matched = [x for x in results if x["matched"] is True]
    assert len(matched) >= 1


def test_evaluate_eu_chatbot_no_matches():
    r = client.post("/domains/eu-ai-act/evaluate", json=EU_FACTS_CHATBOT)
    assert r.status_code == 200
    results = r.json()
    matched = [x for x in results if x["matched"] is True]
    assert len(matched) == 0


def test_evaluate_ndb_all_none():
    facts = {
        "incident_type": "unauthorised_access",
        "data_categories": ["health"],
        "encryption_status": "unencrypted",
        "individuals_affected": "1000+",
        "likely_recipient": "criminal",
        "individual_vulnerability": "health_patients",
    }
    r = client.post("/domains/ndb/evaluate", json=facts)
    assert r.status_code == 200
    results = r.json()
    assert len(results) == 54
    assert all(x["matched"] is None for x in results)


def test_evaluate_unknown_domain_404():
    r = client.post("/domains/invalid/evaluate", json={})
    assert r.status_code == 404


def test_get_rules_unknown_domain_404():
    r = client.get("/domains/invalid/rules")
    assert r.status_code == 404
