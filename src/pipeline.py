"""
Extraction pipeline CLI.

Usage:
  python -m src.pipeline --domain eu-ai-act --source data/eu-ai-act.html
  python -m src.pipeline --domain ndb --source data/ndb.html
"""
import argparse
import json
import os
from datetime import date
from pathlib import Path

import anthropic


def _load_env(path: str = ".env") -> None:
    """Load key=value pairs from a .env file into os.environ (if not already set)."""
    env_file = Path(path)
    if not env_file.exists():
        return
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

from src.ingest import chunk_by_article, chunk_by_section_akn, chunk_by_schedule_clause, extract_article_text, extract_section_text_akn
from src.extract import extract_rules_from_chunk
from src.provenance import verify_docref
from src.schema import DomainFile, Rule

DOMAIN_META = {
    "eu-ai-act": {
        "version": "Regulation (EU) 2024/1689",
        "source_url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689",
        "definitions_article_id": "article-3",
        "source_type": "html",
    },
    "ndb": {
        "version": "Privacy Act 1988 (Cth), ss.26WA-26WR",
        "source_url": "https://www.legislation.gov.au/Details/C2024C00091",
        "definitions_article_id": None,
        "source_type": "html",
    },
    "privacy-apps": {
        "version": "Privacy Act 1988 (Cth), Schedule 1 (APPs 1-13)",
        "source_url": "https://www.legislation.gov.au/Details/C2024C00091",
        "corpus_filename": "privacy-act-1988.xml",
        "definitions_section_num": None,
        "chunk_strategy": "schedule_clause",
        "source_type": "akn",
    },
    "ssa-bereavement": {
        "version": "Social Security Act 1991 (Cth) — bereavement provisions",
        "source_url": "https://www.legislation.gov.au/Details/C2024C00091",
        "corpus_filename": "social-security-act-1991.xml",
        "definitions_section_num": "21",
        "chunk_strategy": "section",
        "source_type": "akn",
    },
    "sis-death-benefits": {
        "version": "Superannuation Industry (Supervision) Act 1993 (Cth) — death benefit provisions",
        "source_url": "https://www.legislation.gov.au/Details/C2024C00091",
        "corpus_filename": "superannuation-industry-(supervision)-act-1993.xml",
        "definitions_section_num": "68a",
        "chunk_strategy": "section",
        "source_type": "akn",
    },
}

CORPUS_DIR_DEFAULT = Path(__file__).parents[2] / "lex-au" / "repo" / "corpus" / "xml"


def run(domain: str, source_path: str | None, out_dir: str = "rules", corpus_dir: str | None = None) -> None:
    meta = DOMAIN_META[domain]
    client = anthropic.Anthropic()
    corpus_root = Path(corpus_dir) if corpus_dir else CORPUS_DIR_DEFAULT

    if meta["source_type"] == "akn":
        xml_path = corpus_root / meta["corpus_filename"]
        print(f"[1/4] Ingesting {xml_path}")
        xml = xml_path.read_text()
        strategy = meta.get("chunk_strategy", "section")
        chunks = (
            chunk_by_schedule_clause(xml, domain=domain)
            if strategy == "schedule_clause"
            else chunk_by_section_akn(xml, domain=domain)
        )
        definitions = ""
        if meta.get("definitions_section_num"):
            definitions = extract_section_text_akn(xml, meta["definitions_section_num"])[:4000]
    else:
        if not source_path:
            raise ValueError(f"--source is required for HTML domain '{domain}'")
        print(f"[1/4] Ingesting {source_path}")
        with open(source_path) as f:
            html = f.read()
        chunks = chunk_by_article(html, domain=domain)
        definitions = ""
        if meta.get("definitions_article_id"):
            definitions = extract_article_text(html, meta["definitions_article_id"])[:4000]

    print(f"      {len(chunks)} chunks in allowlist")

    print("[2/4] Extracting rules via Claude API")
    all_rules: list[Rule] = []
    for chunk in chunks:
        print(f"      {chunk['article_label']} ...", end=" ", flush=True)
        rules = extract_rules_from_chunk(chunk, definitions, domain=domain, client=client)
        all_rules.extend(rules)
        print(f"{len(rules)} rules")

    print("[3/4] Grounding provenance")
    unverified = []
    for rule in all_rules:
        result = verify_docref(rule.docref, chunks)
        if not result.verified:
            unverified.append(rule.rule_id)
            print(f"      WARNING: unverified docref for {rule.rule_id}: {result.note}")

    print("[4/4] Writing output")
    out_path = Path(out_dir) / f"{domain}.json"
    review_path = Path(out_dir) / f"{domain}.REVIEW.md"

    domain_file = DomainFile(
        domain=domain,
        version=meta["version"],
        extracted_at=date.today().isoformat(),
        source_url=meta["source_url"],
        rules=all_rules,
        scenarios=[],
    )
    out_path.write_text(domain_file.model_dump_json(indent=2))

    lines = [
        f"# {domain} — Extraction Review\n\n",
        f"*{len(all_rules)} rules extracted. Review JSON Logic conditions before committing.*\n\n",
    ]
    for rule in all_rules:
        lines.append(f"## [{rule.codifiability.upper()}] {rule.label}\n\n")
        lines.append(f"- **Rule ID:** `{rule.rule_id}`\n")
        lines.append(f"- **Docref:** {rule.docref.article} {rule.docref.section} — [source]({rule.docref.url})\n")
        lines.append(f"- **Condition:** `{json.dumps(rule.condition)}`\n")
        lines.append(f"- **Obligation:** {rule.obligation}\n\n")
        if rule.rule_id in unverified:
            lines.append("> WARNING: Docref unverified — check article citation\n\n")
    review_path.write_text("".join(lines))

    print(f"\nDone. Rules: {out_path}\nReview:  {review_path}")
    if unverified:
        print(f"\nWARNING: {len(unverified)} rules have unverified docrefs: {unverified}")


if __name__ == "__main__":
    _load_env()
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", required=True, choices=list(DOMAIN_META))
    parser.add_argument("--source", default=None, help="HTML source file (required for HTML domains)")
    parser.add_argument("--corpus-dir", default=None, help="Override path to lex-au corpus/xml/")
    parser.add_argument("--out-dir", default="rules")
    args = parser.parse_args()
    run(args.domain, args.source, args.out_dir, args.corpus_dir)
