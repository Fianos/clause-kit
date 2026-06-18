import json
from pathlib import Path

from fastapi import Body, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.engine import evaluate_all
from src.schema import DomainFile, RuleResult

app = FastAPI(title="ClauseKit API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

RULES_DIR = Path("rules")


def _load_domain(domain: str) -> DomainFile:
    path = RULES_DIR / f"{domain}.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Domain '{domain}' not found")
    return DomainFile.model_validate_json(path.read_text())


@app.get("/domains")
def list_domains() -> list[str]:
    return sorted(p.stem for p in RULES_DIR.glob("*.json"))


@app.get("/domains/{domain}/rules")
def get_rules(domain: str) -> DomainFile:
    return _load_domain(domain)


@app.get("/domains/{domain}/scenarios")
def get_scenarios(domain: str) -> list[dict]:
    df = _load_domain(domain)
    return [s.model_dump() for s in df.scenarios]


@app.post("/domains/{domain}/evaluate")
def evaluate(domain: str, facts: dict = Body(...)) -> list[RuleResult]:
    df = _load_domain(domain)
    return evaluate_all(df.rules, facts)
