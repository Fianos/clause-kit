# ClauseKit

Convert legislation into evaluatable rules using an LLM extraction pipeline. Runs conditions as [JSON Logic](https://jsonlogic.com/) against a typed fact schema, with provenance grounding back to the source article.

Two domains shipped:

| Domain | Source | Rules | Scenarios |
|---|---|---|---|
| EU AI Act | Regulation (EU) 2024/1689, Arts 5, 6, Annex I, III | 32 | 5 |
| NDB scheme | Privacy Act 1988 (Cth), ss.26WA-26WR | 54 | 4 |

## Architecture

```
legislation HTML
      │
   ingest.py          chunk by article (allowlist-filtered)
      │
   extract.py         Claude claude-opus-4-8 → Rule[] (JSON Logic conditions)
      │
   provenance.py      verify each docref against source chunks
      │
   rules/{domain}.json + rules/{domain}.REVIEW.md
      │
   api.py             FastAPI  GET /domains/{d}/rules  POST /domains/{d}/evaluate
      │
   web/               Vue 3 sandbox UI (fact form → matched rules)
```

## Setup

Python 3.12+ required.

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
# add ANTHROPIC_API_KEY to .env
```

**json-logic patch:** The `json-logic` 0.6.2 package ships Python 2 code (`dict.keys()[0]`). After creating the venv, patch line ~21 of `.venv/lib/python3.x/site-packages/json_logic/__init__.py`:

```python
# before
op = data.keys()[0]
# after
op = list(data.keys())[0]
```

If you recreate the venv, re-apply this patch. The engine will fail at runtime without it.

## Run the extraction pipeline

Pre-built rule sets are committed to `rules/`. Re-run extraction only if you change the source HTML or prompt:

```bash
python -m src.pipeline --domain eu-ai-act --source data/eu-ai-act.html
python -m src.pipeline --domain ndb --source data/ndb.html
```

Source HTML files are gitignored. Download them separately:

- EU AI Act: [EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32024R1689)
- NDB scheme: legislation.gov.au EPUB HTML (Privacy Act 1988, series C2004A03712)

## Run tests

```bash
.venv/bin/pytest          # 15 tests
.venv/bin/pytest -v       # verbose
```

## Rule format

Each rule in `rules/{domain}.json`:

```json
{
  "rule_id": "eu-ai-act-001",
  "label": "Prohibited: Real-time remote biometric identification in public spaces",
  "condition": {"and": [{"var": "real_time_biometric"}, {"var": "publicly_accessible_spaces"}]},
  "obligation": "Prohibited unless Article 5(1)(a) exceptions apply",
  "scope": "Deployers of AI systems",
  "exceptions": ["Law enforcement with prior judicial authorisation"],
  "codifiability": "high",
  "docref": {
    "source_doc": "EU AI Act",
    "article": "Article 5",
    "section": "5(1)(a)",
    "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689",
    "provision_uri": "http://data.europa.eu/eli/reg/2024/1689/art_5/par_1"
  }
}
```

`condition` is null for `codifiability: "low"` rules (vague standard, not mechanically evaluable). `provision_uri` uses [ELI](https://eur-lex.europa.eu/eli-register/about.html) for EU legislation and [AKN FRBR](https://docs.oasis-open.org/legaldocml/akn-core/v1.0/akn-core-v1.0.html) for Australian legislation.

## Limitations

**JSON Logic expressiveness ceiling.** JSON Logic (`==`, `in`, `and`, `or`, `var`) cannot represent:
- Temporal constraints (obligations with deadlines or sequencing)
- Modal operators (obligatory / permitted / prohibited)
- Defeasibility (rule A applies *unless* rule B overrides it)
- Role-relative obligations (same provision applying differently to providers vs deployers)

Provisions requiring these constructs are classified `low` codifiability and return `matched: null`.

**Fact schema bounds expressiveness.** The fact schema is defined before extraction runs. The LLM can only produce conditions over the variables in the schema — it cannot discover new variables. Rules whose trigger conditions fall outside the schema are classified `low` regardless of their legislative clarity.

**Codifiability is LLM-assigned, not human-validated.** Classifications have not been independently verified against the source legislation by domain experts.

**Not a compliance tool.** ClauseKit is a demonstration of a pipeline, not legal advice. `matched: true` means the rule's coded condition fired — it does not mean you have a legal obligation. Consult a lawyer.

## Project status

- [x] Ingestion (EUR-Lex HTML, legislation.gov.au EPUB)
- [x] LLM extraction with JSON Logic conditions
- [x] Provenance grounding
- [x] Pre-built rule sets for EU AI Act and NDB
- [x] FastAPI evaluation endpoint (`src/api.py`)
- [x] Vue 3 sandbox UI (`web/`)
- [x] Playwright E2E tests
