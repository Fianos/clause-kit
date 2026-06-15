from src.provenance import verify_docref, GroundingResult
from src.schema import Docref

CHUNKS = [
    {"article_id": "article-5", "article_label": "Article 5", "text": "Article 5\nReal-time biometric identification is prohibited."},
    {"article_id": "annex-iii", "article_label": "Annex III", "text": "Annex III\n1. Employment screening systems."},
]

def test_verify_docref_match():
    docref = Docref(source_doc="EU AI Act", article="Article 5", section="1", url="https://example.com")
    result = verify_docref(docref, CHUNKS)
    assert result.verified is True
    assert result.matched_article_id == "article-5"

def test_verify_docref_mismatch():
    docref = Docref(source_doc="EU AI Act", article="Article 99", section="1", url="https://example.com")
    result = verify_docref(docref, CHUNKS)
    assert result.verified is False
    assert result.matched_article_id is None

def test_verify_docref_annex():
    docref = Docref(source_doc="EU AI Act", article="Annex III", section="1", url="https://example.com")
    result = verify_docref(docref, CHUNKS)
    assert result.verified is True
    assert result.matched_article_id == "annex-iii"
