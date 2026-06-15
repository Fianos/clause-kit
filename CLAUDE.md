# ClauseKit

LLM-to-Rules-as-Code pipeline demo. See spec at:
docs/superpowers/specs/2026-06-14-clausekit-design.md

## Running locally

```bash
# Backend
cd projects/clause-kit/repo
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env  # add ANTHROPIC_API_KEY
uvicorn src.api:app --reload

# Frontend (separate terminal)
cd web && npm install && npm run dev
```

## Running extraction pipeline

```bash
python -m src.pipeline --domain eu-ai-act
python -m src.pipeline --domain ndb
```

## Running tests

```bash
pytest                     # all tests
pytest tests/test_api.py   # API only
```

## Rule engine backend

GoRules has no macOS wheel — engine uses `json_logic.jsonLogic` (PyPI: `json-logic`).

**Known issue:** `json-logic` 0.6.2 ships Python 2 code (`dict.keys()[0]`). The venv's
`json_logic/__init__.py` has been patched with `list(dict.keys())[0]`. If you recreate
the venv, re-apply this patch or the engine will fail. The patch is on line ~21 of
`.venv/lib/python3.x/site-packages/json_logic/__init__.py`.

## HTML ingestion

pypandoc requires the `pandoc` binary which is not available in this environment.
All HTML parsing uses BeautifulSoup (`beautifulsoup4`) directly. Do not add pypandoc
calls to ingest.py — use BeautifulSoup.

## Scope

EU AI Act scope: Articles 5, 6, Annex I, Annex III only.
NDB scope: Privacy Act ss.26WA-26WR only.
The article allowlist is enforced in src/ingest.py.
