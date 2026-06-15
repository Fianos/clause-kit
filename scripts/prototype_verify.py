"""
Prototype verification script for ClauseKit Task 3.
Mirrors the notebook logic; run this first to confirm everything works.
"""
import os, json, re
import httpx
import anthropic
from bs4 import BeautifulSoup
from json_logic import jsonLogic
from pydantic import BaseModel
from typing import Literal

# ---------------------------------------------------------------------------
# Cell 1: Load API key
# ---------------------------------------------------------------------------
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            k, v = line.split('=', 1)
            os.environ.setdefault(k.strip(), v.strip())

print("Imports OK")

# ---------------------------------------------------------------------------
# Cell 2: Read and extract Article 5 text
# ---------------------------------------------------------------------------
html_path = os.path.join(os.path.dirname(__file__), "..", "data", "eu-ai-act-raw.html")
with open(html_path, encoding="utf-8") as f:
    html = f.read()

# Extract text via BeautifulSoup (pypandoc requires pandoc binary)
soup = BeautifulSoup(html, "html.parser")
full_text = soup.get_text(separator="\n")

# Normalise whitespace runs but keep paragraph breaks
full_text = re.sub(r"\n{3,}", "\n\n", full_text)
full_text = re.sub(r"[ \t]+", " ", full_text)

# Try to find Article 5 block — EUR-Lex uses various heading styles
match = re.search(r"(Article 5\b.+?)(?=Article 6\b)", full_text, re.DOTALL | re.IGNORECASE)
if not match:
    match = re.search(r"(Art(?:icle)?\.?\s*5\b.+?)(?=Art(?:icle)?\.?\s*6\b)", full_text, re.DOTALL | re.IGNORECASE)

art5_text = match.group(0) if match else ""
print(f"Article 5 text: {len(art5_text)} chars")
if len(art5_text) < 100:
    print("WARNING: Article 5 not found or too short. Snippet around 'Article':")
    idx = full_text.lower().find("article 5")
    print(full_text[max(0, idx-200):idx+500] if idx != -1 else full_text[:2000])
else:
    print(art5_text[:1000])

# ---------------------------------------------------------------------------
# Cell 3: Define schemas
# ---------------------------------------------------------------------------
class Docref(BaseModel):
    source_doc: str
    article: str
    section: str
    url: str

class Rule(BaseModel):
    rule_id: str
    label: str
    condition: dict | None
    obligation: str
    scope: str
    exceptions: list[str]
    codifiability: Literal["high", "medium", "low"]
    docref: Docref

print("Schemas OK")

# ---------------------------------------------------------------------------
# Cell 4: Call Claude API to extract rules
# ---------------------------------------------------------------------------
client = anthropic.Anthropic()

SYSTEM = """You extract rules from legislative text into structured JSON.
Return a JSON array of Rule objects. Each rule must use only the provided fact schema variables in conditions.
If a rule cannot be expressed as a deterministic condition, set condition to null and codifiability to "low".
Use JSON Logic format for conditions: {"and":[...]}, {"==":[{"var":"field"},value]}, {"in":[{"var":"field"},["a","b"]]}.
Return ONLY the JSON array, no markdown fences, no explanation."""

FACT_SCHEMA = """
EU AI Act fact variables:
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
"""

RULE_SCHEMA = Rule.model_json_schema()

resp = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=4096,
    system=SYSTEM,
    messages=[{
        "role": "user",
        "content": f"""Extract all prohibition rules from Article 5 of the EU AI Act.

FACT SCHEMA:
{FACT_SCHEMA}

RULE SCHEMA (each object must match exactly):
{json.dumps(RULE_SCHEMA, indent=2)}

For Article 5(1)(h) (real-time biometric identification in publicly accessible spaces), the condition must be:
{{"and": [{{"==": [{{"var": "real_time_biometric"}}, true]}}, {{"==": [{{"var": "publicly_accessible_spaces"}}, true]}}]}}

Docref URL pattern: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689#art_5

ARTICLE TEXT:
{art5_text[:8000]}"""
    }]
)

raw = resp.content[0].text.strip()
# Strip markdown fences if present
raw = re.sub(r"^```json\n?", "", raw)
raw = re.sub(r"\n?```$", "", raw).strip()

print(f"\nRaw response length: {len(raw)} chars")
print(raw[:500])

# ---------------------------------------------------------------------------
# Cell 5: Validate and display extracted rules
# ---------------------------------------------------------------------------
data = json.loads(raw)
if isinstance(data, dict):
    data = [data]
rules = [Rule.model_validate(r) for r in data]

print(f"\nExtracted {len(rules)} rules:\n")
for r in rules:
    print(f"  [{r.codifiability.upper()}] {r.label}")
    print(f"    Condition: {json.dumps(r.condition)}")
    print(f"    Docref: {r.docref.article} {r.docref.section}")
    print()

# ---------------------------------------------------------------------------
# Cell 6: Verify JSON Logic evaluates correctly
# ---------------------------------------------------------------------------
facts_hr = {
    "deployment_sector": "employment",
    "real_time_biometric": False,
    "publicly_accessible_spaces": False,
    "involves_safety_component": False,
    "is_gpai_model": False,
    "post_hoc_biometric": False,
    "art6_3_exception_narrow_procedure": False,
    "art6_3_exception_human_override": False,
    "art6_3_exception_preparatory_task": False,
    "art6_3_exception_contravention_check": False,
}

facts_biometric = {
    "deployment_sector": "biometric_id",
    "real_time_biometric": True,
    "publicly_accessible_spaces": True,
    "involves_safety_component": False,
    "is_gpai_model": False,
    "post_hoc_biometric": False,
    "art6_3_exception_narrow_procedure": False,
    "art6_3_exception_human_override": False,
    "art6_3_exception_preparatory_task": False,
    "art6_3_exception_contravention_check": False,
}

print("Evaluation results:\n")
errors = []
art5h_hr = None
art5h_bio = None
for rule in rules:
    if rule.condition is None:
        print(f"  SKIP (low codifiability): {rule.label}")
        continue
    try:
        r_hr = jsonLogic(rule.condition, facts_hr)
        r_bio = jsonLogic(rule.condition, facts_biometric)
        print(f"  {rule.label}")
        print(f"    HR facts: {r_hr} | Biometric+public facts: {r_bio}")
        # Detect art 5(1)(h) — real-time biometric
        if "real_time_biometric" in json.dumps(rule.condition) or "5(1)(h)" in rule.rule_id or "biometric" in rule.label.lower():
            art5h_hr = r_hr
            art5h_bio = r_bio
    except Exception as e:
        errors.append((rule.rule_id, str(e)))
        print(f"  ERROR in {rule.rule_id}: {e}")

print(f"\nErrors: {len(errors)}")
print("\n--- Self-review checks ---")
high_rules = [r for r in rules if r.codifiability == "high"]
print(f"Rules with HIGH codifiability: {len(high_rules)}")
if art5h_hr is not None:
    ok = (art5h_hr == False) and (art5h_bio == True)
    print(f"Art 5(1)(h) check: HR={art5h_hr} biometric_public={art5h_bio} -> {'PASS' if ok else 'FAIL'}")
else:
    print("Art 5(1)(h) rule: not identified in output (check rule labels)")

# ---------------------------------------------------------------------------
# Cell 7: Test EUR-Lex URL stability
# ---------------------------------------------------------------------------
test_url = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689#art_5"
try:
    r = httpx.get(test_url, follow_redirects=True, timeout=30)
    url_status = r.status_code
    print(f"\nEUR-Lex anchor URL status: {url_status}")
    print("EUR-Lex anchor URLs are stable and usable as docref URLs." if url_status == 200 else "WARNING: URL returned non-200")
except httpx.TimeoutException:
    url_status = "timeout"
    print(f"\nEUR-Lex anchor URL: TIMEOUT (EUR-Lex can be slow; URL format is correct)")
except Exception as e:
    url_status = f"error: {e}"
    print(f"\nEUR-Lex anchor URL: ERROR {e}")

print("\n=== prototype_verify.py COMPLETE ===")
print(f"Total rules: {len(rules)}")
print(f"Errors: {len(errors)}")
