import re
from bs4 import BeautifulSoup

ALLOWLISTS: dict[str, set[str]] = {
    "eu-ai-act": {"article-5", "article-6", "annex-i", "annex-iii"},
    # legislation.gov.au EPUB section numbers for Privacy Act ss.26WA-26WR
    "ndb": {f"26w{c}" for c in "abcdefghijklmnopqr"},
}

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
