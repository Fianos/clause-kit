# ClauseKit

Convert legislation into evaluatable rules using an LLM extraction pipeline. Runs conditions as [JSON Logic](https://jsonlogic.com/) against a typed fact schema, with provenance grounding back to the source article.

**Status: v0.3.0** - EU AI Act and NDB rules available. Privacy APPs, SSA bereavement, SIS death benefits schemas created but rules not extracted.

## Uses

- **Depends on (AKN domains only):** [lex-au](https://github.com/cchew/lex-au) (AKN 3.0 XML corpus; HTML domains like EU AI Act and NDB ingest directly from source HTML instead, no lex-au dependency)

Full stack map: [lex-au-search's `STACK.md`](https://github.com/cchew/lex-au-search/blob/main/STACK.md) and [lex-au's `FUTURE.md`](https://github.com/cchew/lex-au/blob/main/FUTURE.md).

## Versions

- **v0.3.0** - AKN XML ingest path; Privacy APPs, SSA bereavement, SIS death benefits schemas (extraction deferred).
- **v0.2.0** - AKN vs plain-text comparison mode, validated against NDB s.26WA branching.
- **v0.1.0** - EU AI Act and NDB scheme extraction, JSON Logic engine, provenance grounding, FastAPI, Vue 3 sandbox.

## Domains

| Domain | Source | Rules | Scenarios |
|---|---|---|---|
| EU AI Act | Regulation (EU) 2024/1689, Arts 5, 6, Annex I, III | 32 | 5 |
| NDB scheme | Privacy Act 1988 (Cth), ss.26WA-26WR | 54 | 4 |
| Privacy APPs | Privacy Act 1988 (Cth), Schedule 1 (APPs 1-13) | pending | - |
| SSA bereavement | Social Security Act 1991 (Cth), bereavement provisions | pending | - |
| SIS death benefits | Superannuation Industry (Supervision) Act 1993 (Cth), ss.55A-55C, 68AA-68AAF | pending | - |

## Architecture

```
legislation source
      │
      ├── HTML (EUR-Lex, legislation.gov.au EPUB)
      │         ingest.py → chunk_by_article
      │
      └── AKN XML (lex-au corpus)
                ingest.py → chunk_by_section_akn / chunk_by_schedule_clause
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

AKN XML source files are read from the`corpus/xml/` directory, downloaded directly from [Hugging Face](https://huggingface.co/datasets/cchew/lex-au):

```bash
pip install huggingface_hub
python -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='cchew/lex-au', repo_type='dataset', local_dir='../../lex-au/repo/corpus', allow_patterns='xml/*')"
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

Pre-built rule sets are committed to `rules/`. Re-run extraction only if you change the source or prompt.

**HTML domains** (source file required):

```bash
python -m src.pipeline --domain eu-ai-act --source data/eu-ai-act.html
python -m src.pipeline --domain ndb --source data/ndb.html
```

Source HTML files are gitignored. Download them separately:

- EU AI Act: [EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32024R1689)
- NDB scheme: legislation.gov.au EPUB HTML (Privacy Act 1988, series C2004A03712)

**AKN domains** (reads from lex-au corpus, no `--source` needed):

```bash
python -m src.pipeline --domain privacy-apps
python -m src.pipeline --domain ssa-bereavement
python -m src.pipeline --domain sis-death-benefits
```

## Run tests

```bash
.venv/bin/pytest          # 58 tests
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

**Fact schema bounds expressiveness.** The fact schema is defined before extraction runs. The LLM can only produce conditions over the variables in the schema - it cannot discover new variables. Rules whose trigger conditions fall outside the schema are classified `low` regardless of their legislative clarity.

**Codifiability is LLM-assigned, not human-validated.** Classifications have not been independently verified against the source legislation by domain experts.

**Not a compliance tool.** ClauseKit is a demonstration of a pipeline, not legal advice. `matched: true` means the rule's coded condition fired - it does not mean you have a legal obligation. Consult a lawyer.
