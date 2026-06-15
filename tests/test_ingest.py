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
