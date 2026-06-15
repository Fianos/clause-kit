import json
import re
import anthropic
from src.schema import Rule

DOMAIN_FACT_SCHEMAS = {
    "eu-ai-act": """
Fact variables for EU AI Act:
- deployment_sector: "employment"|"education"|"credit"|"law_enforcement"|"border"|"critical_infra"|"biometric_id"|"general"
- publicly_accessible_spaces: boolean
- involves_safety_component: boolean
- is_gpai_model: boolean
- real_time_biometric: boolean
- post_hoc_biometric: boolean
- art6_3_exception_narrow_procedure: boolean
- art6_3_exception_human_override: boolean
- art6_3_exception_preparatory_task: boolean
- art6_3_exception_contravention_check: boolean
""",
    "ndb": """
Fact variables for NDB scheme:
- incident_type: "unauthorised_access"|"loss"|"unauthorised_disclosure"
- data_categories: array of "health"|"financial"|"identity"|"biometric"|"sensitive"
- encryption_status: "encrypted"|"partial"|"unencrypted"
- individuals_affected: "1-10"|"10-100"|"100-1000"|"1000+"
- likely_recipient: "unknown"|"specific_individual"|"criminal"|"broad_public"
- individual_vulnerability: "general"|"elderly"|"children"|"health_patients"
""",
}

SYSTEM_PROMPT = """You extract legislative rules into structured JSON.
Return a JSON array of rule objects. Each rule must use only the provided fact schema variables in conditions.
If a rule cannot be expressed as a deterministic condition (vague standard, judgment call), set condition to null and codifiability to "low".
Use JSON Logic format for conditions: {"and":[...]}, {"or":[...]}, {"==":[{"var":"field"},value]}, {"in":[{"var":"field"},["a","b"]]}.
Return ONLY the JSON array, no markdown fences."""


def extract_rules_from_chunk(
    chunk: dict,
    definitions: str,
    domain: str,
    client: anthropic.Anthropic | None = None,
) -> list[Rule]:
    if client is None:
        client = anthropic.Anthropic()

    fact_schema = DOMAIN_FACT_SCHEMAS[domain]

    rule_schema = json.dumps(Rule.model_json_schema(), indent=2)

    resp = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=8192,
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": (
                f"DEFINITIONS:\n{definitions}\n\n"
                f"FACT SCHEMA:\n{fact_schema}\n\n"
                f"RULE SCHEMA (each object in the array must match exactly):\n{rule_schema}\n\n"
                f"ARTICLE: {chunk['article_label']}\n\n"
                f"{chunk['text'][:8000]}\n\n"
                "Extract all distinct rules from this article as a JSON array."
            ),
        }],
    )

    raw = resp.content[0].text.strip()
    raw = re.sub(r"^```json\n?", "", raw)
    raw = re.sub(r"\n?```$", "", raw).strip()

    data = json.loads(raw)
    return [Rule.model_validate(r) for r in data]
