import pytest
from src.engine import evaluate_rule, evaluate_all
from src.schema import Rule, Docref


def _rule(condition, codifiability="high"):
    return Rule(
        rule_id="test-001",
        label="Test rule",
        condition=condition,
        obligation="Do something.",
        scope="All providers",
        exceptions=[],
        codifiability=codifiability,
        docref=Docref(
            source_doc="Test Act",
            article="Article 1",
            section="1(a)",
            url="https://example.com",
        ),
    )


def test_evaluate_rule_matched():
    rule = _rule({"==": [{"var": "deployment_sector"}, "law_enforcement"]})
    result = evaluate_rule(rule, {"deployment_sector": "law_enforcement"})
    assert result.matched is True
    assert result.rule_id == "test-001"
    assert result.codifiability == "high"


def test_evaluate_rule_not_matched():
    rule = _rule({"==": [{"var": "deployment_sector"}, "law_enforcement"]})
    result = evaluate_rule(rule, {"deployment_sector": "employment"})
    assert result.matched is False


def test_evaluate_rule_complex_condition():
    rule = _rule({"and": [{"var": "real_time_biometric"}, {"var": "publicly_accessible_spaces"}]})
    assert evaluate_rule(rule, {"real_time_biometric": True, "publicly_accessible_spaces": True}).matched is True
    assert evaluate_rule(rule, {"real_time_biometric": True, "publicly_accessible_spaces": False}).matched is False


def test_evaluate_rule_null_condition_returns_none():
    rule = _rule(condition=None, codifiability="low")
    result = evaluate_rule(rule, {"x": 1})
    assert result.matched is None


def test_evaluate_rule_low_codifiability_skipped_even_with_condition():
    rule = _rule(condition={"==": [{"var": "x"}, 1]}, codifiability="low")
    result = evaluate_rule(rule, {"x": 1})
    assert result.matched is None


def test_evaluate_rule_medium_codifiability_runs():
    rule = _rule(condition={"==": [{"var": "x"}, 1]}, codifiability="medium")
    result = evaluate_rule(rule, {"x": 1})
    assert result.matched is True


def test_evaluate_all_length():
    rules = [
        _rule({"==": [{"var": "x"}, 1]}, "high"),
        _rule(None, "low"),
        _rule({"==": [{"var": "x"}, 2]}, "medium"),
    ]
    results = evaluate_all(rules, {"x": 1})
    assert len(results) == 3
    assert results[0].matched is True
    assert results[1].matched is None
    assert results[2].matched is False


def test_evaluate_all_preserves_rule_metadata():
    rules = [_rule({"==": [{"var": "x"}, 1]})]
    results = evaluate_all(rules, {"x": 1})
    assert results[0].label == "Test rule"
    assert results[0].obligation == "Do something."
    assert results[0].docref.article == "Article 1"
