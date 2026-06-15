import re
from bs4 import BeautifulSoup

ALLOWLISTS: dict[str, set[str]] = {
    "eu-ai-act": {"article-5", "article-6", "annex-i", "annex-iii"},
    "ndb": {f"section-26w{c}" for c in "abcdefghijklmnopqr"},
}

# EUR-Lex uses <p class="oj-ti-art"> for article numbers and
# <p class="oj-doc-ti"> for annex titles instead of h1-h4 elements.
_EURLEX_HEADING_CLASSES = frozenset({"oj-ti-art", "oj-doc-ti"})


def _normalise_id(text: str) -> str:
    """Derive a stable article_id from heading text.

    Handles non-breaking spaces (\\xa0) used in EUR-Lex headings.
    'Article\\xa05' → 'article-5', 'ANNEX\\xa0III' → 'annex-iii'
    """
    text = text.replace("\xa0", " ").lower().strip()
    return re.sub(r"\s+", "-", text)


def _is_section_heading(tag) -> bool:
    """True if tag marks the start of a new article/annex section.

    oj-ti-art (article numbers) always qualify.
    oj-doc-ti only qualifies if the text is an annex title like 'ANNEX I'
    — the same class is reused for subtitles within annexes.
    """
    if not hasattr(tag, "name") or not tag.name:
        return False
    if re.match(r"^h[1-4]$", tag.name):
        return True
    cls = set(tag.get("class", []))
    if "oj-ti-art" in cls:
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
        elif set(tag.get("class", [])) & _EURLEX_HEADING_CLASSES:
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

    # Fall back to normalised text match (covers EUR-Lex dynamic ids)
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

    Works with both simple HTML (h1-h4 with id attributes) and
    EUR-Lex HTML (p.oj-ti-art / p.oj-doc-ti with dynamic ids).
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
