import re
from bs4 import BeautifulSoup

ALLOWLISTS: dict[str, set[str]] = {
    "eu-ai-act": {"article-5", "article-6", "annex-i", "annex-iii"},
    # legislation.gov.au EPUB section numbers for Privacy Act ss.26WA-26WR
    "ndb": {f"26w{c}" for c in "abcdefghijklmnopqr"},
}

# NDB (Privacy Act ss.26WA-26WR) — same as HTML allowlist, AKN source
ALLOWLISTS["ndb-akn"] = ALLOWLISTS["ndb"].copy()

# SSA 1991 — bereavement provisions only
ALLOWLISTS["ssa-bereavement"] = {
    "21",
    "82", "83", "84", "85", "86",
    "146g", "146h", "146i", "146j", "146k",
    "238", "239", "240", "241",
    "514a", "514b", "514c", "514d", "514e",
}

# SIS Act 1993 — death benefit provisions in Part 6
ALLOWLISTS["sis-death-benefits"] = {
    "55a", "55b", "55c",
    "68a", "68aa", "68aaa", "68aab", "68aac", "68aad", "68aae", "68aaf",
}

# Privacy APPs — Schedule 1 APPs 1-13 (grouped by clause number)
ALLOWLISTS["privacy-apps"] = {f"app-{n}" for n in range(1, 14)}

# EUR-Lex uses <p class="oj-ti-art"> for article numbers and
# <p class="oj-doc-ti"> for annex titles instead of h1-h4 elements.
_EURLEX_HEADING_CLASSES = frozenset({"oj-ti-art", "oj-doc-ti"})

# legislation.gov.au EPUB HTML uses <p class="ActHead5"> for section headings.
_LEGSGOV_HEADING_CLASSES = frozenset({"ActHead5"})


def _normalise_id(text: str) -> str:
    """Derive a stable article_id from heading text.

    For legislation.gov.au section headings like '26WE Eligible data breach',
    extracts the section number only ('26we').
    For EUR-Lex headings like 'Article\xa05' → 'article-5', 'ANNEX\xa0III' → 'annex-iii'.
    """
    text = text.replace("\xa0", " ").lower().strip()
    # legislation.gov.au: first token is a section number like '26we', '26wg'
    first = text.split()[0] if text else ""
    if re.match(r"^\d+[a-z]+$", first):
        return first
    return re.sub(r"\s+", "-", text)


def _is_section_heading(tag) -> bool:
    """True if tag marks the start of a new article/annex/section boundary.

    Recognises:
    - Standard h1-h4 elements
    - EUR-Lex: p.oj-ti-art (always) and p.oj-doc-ti (only for 'ANNEX ...' titles)
    - legislation.gov.au EPUB: p.ActHead5
    """
    if not hasattr(tag, "name") or not tag.name:
        return False
    if re.match(r"^h[1-4]$", tag.name):
        return True
    cls = set(tag.get("class", []))
    if "oj-ti-art" in cls or cls & _LEGSGOV_HEADING_CLASSES:
        return True
    if "oj-doc-ti" in cls:
        txt = tag.get_text(" ", strip=True).replace("\xa0", " ").strip()
        return bool(re.match(r"^ANNEX\s", txt, re.IGNORECASE))
    return False


def _find_all_headings(soup: BeautifulSoup) -> list:
    """Return all heading elements in document order."""
    headings = []
    for tag in soup.find_all(True):
        if not hasattr(tag, "name") or not tag.name:
            continue
        if re.match(r"^h[1-4]$", tag.name):
            headings.append(tag)
        elif set(tag.get("class", [])) & (_EURLEX_HEADING_CLASSES | _LEGSGOV_HEADING_CLASSES):
            headings.append(tag)
    return headings


def _collect_text(heading) -> str:
    """Collect all text from heading until next section heading."""
    label = heading.get_text(" ", strip=True).replace("\xa0", " ")
    parts = [label]
    for sibling in heading.next_siblings:
        if _is_section_heading(sibling):
            break
        if hasattr(sibling, "get_text"):
            text = sibling.get_text(" ", strip=True)
            if text:
                parts.append(text)
    return "\n".join(parts)


def _section_num_to_id(num_text: str) -> str:
    """Normalise AKN <num> text to a stable article_id."""
    return re.sub(r"\s+", "", num_text.lower()).strip(".")


def chunk_by_section_akn(xml: str, domain: str) -> list[dict]:
    """Parse AKN XML → list of {article_id, article_label, text, section_eid} dicts.

    Finds <section> elements, normalises <num> to article_id,
    filters by domain allowlist.
    """
    allowed = ALLOWLISTS[domain]
    soup = BeautifulSoup(xml, "html.parser")

    chunks = []
    for section in soup.find_all("section"):
        num_tag = section.find("num", recursive=False)
        if num_tag is None:
            continue
        num_text = num_tag.get_text(strip=True)
        article_id = _section_num_to_id(num_text)

        if article_id not in allowed:
            continue

        heading_tag = section.find("heading", recursive=False)
        label_parts = [num_text]
        if heading_tag:
            label_parts.append(heading_tag.get_text(strip=True))
        label = "  ".join(label_parts)

        text = re.sub(r"\s+", " ", section.get_text(" ", strip=True)).strip()
        chunks.append({
            "article_id": article_id,
            "article_label": label,
            "text": text,
            "section_eid": section.get("eid", ""),
        })

    return chunks


def chunk_by_schedule_clause(xml: str, domain: str) -> list[dict]:
    """Parse AKN Schedule 1 (APPs) XML → one chunk per APP (1-13).

    Groups hcontainer[name=subclause] elements by integer prefix of <num>.
    """
    allowed = ALLOWLISTS[domain]
    soup = BeautifulSoup(xml, "html.parser")

    schedule = soup.find(attrs={"eid": "schedule-1"})
    if schedule is None:
        return []

    app_chunks: dict[str, list[str]] = {}
    for hc in schedule.find_all("hcontainer", attrs={"name": "subclause"}):
        num_tag = hc.find("num", recursive=False)
        if num_tag is None:
            continue
        num_text = num_tag.get_text(strip=True)
        app_num = num_text.split(".")[0]
        app_key = f"app-{app_num}"
        if app_key not in allowed:
            continue
        text = re.sub(r"\s+", " ", hc.get_text(" ", strip=True)).strip()
        app_chunks.setdefault(app_key, []).append(text)

    chunks = []
    for app_key in sorted(app_chunks.keys(), key=lambda k: int(k.split("-")[1])):
        app_num = app_key.split("-")[1]
        label = f"Australian Privacy Principle {app_num}"
        combined = "\n\n".join(app_chunks[app_key])
        chunks.append({
            "article_id": app_key,
            "article_label": label,
            "text": combined,
            "section_eid": f"schedule-1/clause-{app_num}",
        })

    return chunks


def extract_section_text_akn(xml: str, section_num: str) -> str:
    """Extract plain text for a specific section by its <num> value."""
    soup = BeautifulSoup(xml, "html.parser")
    target = section_num.lower().strip(".")
    for section in soup.find_all("section"):
        num_tag = section.find("num", recursive=False)
        if num_tag is None:
            continue
        if _section_num_to_id(num_tag.get_text(strip=True)) == target:
            return re.sub(r"\s+", " ", section.get_text(" ", strip=True)).strip()
    return ""


def extract_article_text(html: str, article_id: str) -> str:
    """Extract text for a specific article regardless of allowlist.

    Finds by id attribute first (simple HTML), then by normalised text
    (EUR-Lex HTML where ids are dynamic like 'd1e2090-1-1').
    """
    soup = BeautifulSoup(html, "html.parser")

    # Try id attribute match first
    heading = soup.find(id=article_id)
    if heading is None:
        for tag in soup.find_all(True):
            if tag.get("id", "").lower() == article_id.lower():
                heading = tag
                break

    # Fall back to normalised text match
    if heading is None:
        for tag in _find_all_headings(soup):
            if _normalise_id(tag.get_text(" ", strip=True)) == article_id:
                heading = tag
                break

    if not heading:
        return ""
    return _collect_text(heading)


def chunk_by_article(html: str, domain: str) -> list[dict]:
    """Parse HTML → list of {article_id, article_label, text} dicts.

    Works with simple HTML (h1-h4 with id attributes), EUR-Lex HTML
    (p.oj-ti-art / p.oj-doc-ti), and legislation.gov.au EPUB HTML (p.ActHead5).
    Only articles in the domain allowlist are returned.
    """
    allowed = ALLOWLISTS[domain]
    soup = BeautifulSoup(html, "html.parser")

    chunks = []
    for heading in _find_all_headings(soup):
        label = heading.get_text(" ", strip=True).replace("\xa0", " ")
        article_id = _normalise_id(label)

        # For simple HTML, prefer the explicit id attribute if it's in the allowlist
        id_attr = heading.get("id", "").lower()
        if id_attr and id_attr in allowed:
            article_id = id_attr

        if article_id not in allowed:
            continue

        text = _collect_text(heading)
        if text:
            chunks.append({
                "article_id": article_id,
                "article_label": label,
                "text": text,
            })

    return chunks
