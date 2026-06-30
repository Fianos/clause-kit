import pytest
from src.ingest import chunk_by_article, ALLOWLISTS


def test_eu_allowlist_contains_expected_articles():
    allowed = ALLOWLISTS["eu-ai-act"]
    assert "article-5" in allowed
    assert "article-6" in allowed
    assert "annex-iii" in allowed
    assert "article-9" not in allowed  # obligations excluded


def test_chunk_by_article_returns_chunks_with_metadata():
    sample_html = """
    <html><body>
    <h2 id="article-5">Article 5</h2>
    <p>Prohibited practices content.</p>
    <h2 id="article-6">Article 6</h2>
    <p>High-risk classification content.</p>
    <h2 id="article-9">Article 9</h2>
    <p>Risk management content.</p>
    </body></html>
    """
    chunks = chunk_by_article(sample_html, domain="eu-ai-act")
    ids = [c["article_id"] for c in chunks]
    assert "article-5" in ids
    assert "article-6" in ids
    assert "article-9" not in ids  # blocked by allowlist


def test_chunk_preserves_text():
    sample_html = """
    <html><body>
    <h2 id="article-5">Article 5</h2>
    <p>Prohibited practices content here.</p>
    </body></html>
    """
    chunks = chunk_by_article(sample_html, domain="eu-ai-act")
    art5 = next(c for c in chunks if c["article_id"] == "article-5")
    assert "Prohibited practices" in art5["text"]


from src.ingest import chunk_by_section_akn, extract_section_text_akn

MINIMAL_AKN_SECTIONS = """\
<?xml version="1.0" encoding="UTF-8"?>
<akomaNtoso xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
  <act>
    <body>
      <section eId="part-A__sec-26WA">
        <num>26WA</num>
        <heading>Eligible data breaches</heading>
        <content><p>There is an eligible data breach if there is unauthorised access.</p></content>
      </section>
      <section eId="part-A__sec-26WB">
        <num>26WB</num>
        <heading>Meaning of entity</heading>
        <content><p>An entity is an APP entity that holds personal information.</p></content>
      </section>
      <section eId="part-A__sec-99">
        <num>99</num>
        <heading>Other section</heading>
        <content><p>Not in allowlist.</p></content>
      </section>
    </body>
  </act>
</akomaNtoso>"""


def test_chunk_by_section_akn_filters_by_allowlist():
    chunks = chunk_by_section_akn(MINIMAL_AKN_SECTIONS, domain="ndb")
    ids = [c["article_id"] for c in chunks]
    assert "26wa" in ids
    assert "26wb" in ids
    assert "99" not in ids


def test_chunk_by_section_akn_includes_section_eid():
    chunks = chunk_by_section_akn(MINIMAL_AKN_SECTIONS, domain="ndb")
    c = next(c for c in chunks if c["article_id"] == "26wa")
    assert c["section_eid"] == "part-A__sec-26WA"


def test_chunk_by_section_akn_label_includes_num_and_heading():
    chunks = chunk_by_section_akn(MINIMAL_AKN_SECTIONS, domain="ndb")
    c = next(c for c in chunks if c["article_id"] == "26wa")
    assert "26WA" in c["article_label"]
    assert "Eligible data breaches" in c["article_label"]


def test_chunk_by_section_akn_text_contains_content():
    chunks = chunk_by_section_akn(MINIMAL_AKN_SECTIONS, domain="ndb")
    c = next(c for c in chunks if c["article_id"] == "26wa")
    assert "eligible data breach" in c["text"]
    assert "unauthorised access" in c["text"]


def test_extract_section_text_akn_returns_content():
    text = extract_section_text_akn(MINIMAL_AKN_SECTIONS, "26WB")
    assert "APP entity" in text


def test_extract_section_text_akn_missing_returns_empty():
    text = extract_section_text_akn(MINIMAL_AKN_SECTIONS, "999")
    assert text == ""
