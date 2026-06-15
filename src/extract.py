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

# Provision URI guidance per domain for the docref.provision_uri field.
# EU AI Act uses ELI (European Legislation Identifier).
# Australian NDB scheme uses AKN FRBR URI (Akoma Ntoso / OASIS LegalDocML).
DOMAIN_PROVISION_URI_GUIDANCE = {
    "eu-ai-act": """
provision_uri: ELI URI for this provision. Format: http://data.europa.eu/eli/reg/2024/1689/{fragment}
Examples:
  Article 5      → http://data.europa.eu/eli/reg/2024/1689/art_5
  Article 5(1)   → http://data.europa.eu/eli/reg/2024/1689/art_5/par_1
  Article 6      → http://data.europa.eu/eli/reg/2024/1689/art_6
  Annex I        → http://data.europa.eu/eli/reg/2024/1689/anx_1
  Annex III      → http://data.europa.eu/eli/reg/2024/1689/anx_3
""",
    "ndb": """
provision_uri: AKN FRBR URI (Akoma Ntoso) for this provision. Format: /akn/au/act/1988-119/{fragment}
The Privacy Act 1988 is Act No. 119 of 1988.
Examples:
  Section 26WA   → /akn/au/act/1988-119/section/26WA
  Section 26WE   → /akn/au/act/1988-119/section/26WE
  Section 26WG   → /akn/au/act/1988-119/section/26WG
  Section 26WL   → /akn/au/act/1988-119/section/26WL
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
    provision_uri_guidance = DOMAIN_PROVISION_URI_GUIDANCE[domain]
    rule_schema = json.dumps(Rule.model_json_schema(), indent=2)

    resp = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=8192,
        temperature=0,
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": (
                f"DEFINITIONS:\n{definitions}\n\n"
                f"FACT SCHEMA:\n{fact_schema}\n\n"
                f"PROVISION URI GUIDANCE:\n{provision_uri_guidance}\n\n"
                f"RULE SCHEMA (each object in the array must match exactly):\n{rule_schema}\n\n"
                f"ARTICLE: {chunk['article_label']}\n\n"
                f"{chunk['text'][:8000]}\n\n"
                "Extract all distinct rules from this article as a JSON array. "
                "Populate provision_uri for every rule using the guidance above."
            ),
        }],
    )

    raw = resp.content[0].text.strip()
    raw = re.sub(r"^```json\n?", "", raw)
    raw = re.sub(r"\n?```$", "", raw).strip()

    data = json.loads(raw)
    return [Rule.model_validate(r) for r in data]
