from __future__ import annotations
import re
import warnings
from pathlib import Path
import anthropic
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
from src.extract import extract_rules_from_chunk
from src.schema import ComparisonResult

_AKN_GUIDANCE = (
    "The following provision is in AKN (Akoma Ntoso) XML. "
    "eId attributes identify provisions; <term> tags mark defined terms; "
    "<ref href> tags mark cross-references. "
    "Use eId values as section identifiers in provision_uri."
)


def _strip_xml_tags(xml: str) -> str:
    text = re.sub(r"<[^>]+>", " ", xml)
    return re.sub(r"\s+", " ", text).strip()


def _extract_label(xml: str) -> str:
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
        soup = BeautifulSoup(xml, "html.parser")
    num = soup.find("num")
    heading = soup.find("heading")
    parts = []
    if num:
        parts.append(num.get_text(strip=True))
    if heading:
        parts.append(heading.get_text(strip=True))
    return " ".join(parts) if parts else "Section"


def run_comparison(
    section_id: str,
    domain: str,
    data_dir: str | Path = "data/compare",
    client: anthropic.Anthropic | None = None,
) -> ComparisonResult:
    if client is None:
        client = anthropic.Anthropic()

    xml_path = Path(data_dir) / f"{domain}-{section_id}.xml"
    if not xml_path.exists():
        raise FileNotFoundError(f"No AKN XML for {domain}/{section_id} at {xml_path}")

    section_xml = xml_path.read_text()
    article_label = _extract_label(section_xml)

    plain_chunk = {
        "article_id": section_id,
        "article_label": article_label,
        "text": _strip_xml_tags(section_xml),
    }
    akn_chunk = {
        "article_id": section_id,
        "article_label": article_label,
        "text": f"{_AKN_GUIDANCE}\n\n{section_xml}",
    }

    plain_rules = extract_rules_from_chunk(plain_chunk, definitions="", domain=domain, client=client)
    akn_rules = extract_rules_from_chunk(akn_chunk, definitions="", domain=domain, client=client)

    return ComparisonResult(
        domain=domain,
        section_id=section_id,
        plain_rules=plain_rules,
        akn_rules=akn_rules,
    )
