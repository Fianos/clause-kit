from json_logic import jsonLogic
from src.schema import Rule, RuleResult


def evaluate_rule(rule: Rule, facts: dict) -> RuleResult:
    if rule.condition is None or rule.codifiability == "low":
        matched = None
    else:
        try:
            matched = bool(jsonLogic(rule.condition, facts))
        except Exception:
            matched = None
    return RuleResult(
        rule_id=rule.rule_id,
        matched=matched,
        codifiability=rule.codifiability,
        label=rule.label,
        obligation=rule.obligation,
        docref=rule.docref,
    )


def evaluate_all(rules: list[Rule], facts: dict) -> list[RuleResult]:
    return [evaluate_rule(r, facts) for r in rules]
