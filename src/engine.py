from json_logic import jsonLogic
from src.schema import Rule, RuleResult


def _extract_vars(condition: object) -> list[str]:
    if isinstance(condition, dict):
        if "var" in condition:
            v = condition["var"]
            return [v] if isinstance(v, str) and v else []
        return [
            var
            for val in condition.values()
            for var in _extract_vars(val)
        ]
    if isinstance(condition, list):
        return [var for item in condition for var in _extract_vars(item)]
    return []


def evaluate_rule(rule: Rule, facts: dict) -> RuleResult:
    if rule.condition is None or rule.codifiability == "low":
        matched = None
    else:
        try:
            matched = bool(jsonLogic(rule.condition, facts))
        except Exception:
            matched = None
    if matched is not None and rule.condition is not None:
        var_names = _extract_vars(rule.condition)
        matched_facts = {k: facts.get(k) for k in dict.fromkeys(var_names) if k in facts}
    else:
        matched_facts = None
    return RuleResult(
        rule_id=rule.rule_id,
        matched=matched,
        codifiability=rule.codifiability,
        label=rule.label,
        obligation=rule.obligation,
        docref=rule.docref,
        matched_facts=matched_facts,
    )


def evaluate_all(rules: list[Rule], facts: dict) -> list[RuleResult]:
    return [evaluate_rule(r, facts) for r in rules]
