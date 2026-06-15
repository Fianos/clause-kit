import re
from dataclasses import dataclass
from src.schema import Docref


@dataclass
class GroundingResult:
    verified: bool
    matched_article_id: str | None
    note: str = ""


def _normalise(text: str) -> str:
    return re.sub(r"[\s\-]+", " ", text.lower()).strip()


def verify_docref(docref: Docref, chunks: list[dict]) -> GroundingResult:
    """Check that docref.article matches a chunk in the source."""
    needle = _normalise(docref.article)
    for chunk in chunks:
        label = _normalise(chunk["article_label"])
        text = _normalise(chunk["text"])
        if needle in label or needle in text:
            return GroundingResult(verified=True, matched_article_id=chunk["article_id"])
    return GroundingResult(
        verified=False,
        matched_article_id=None,
        note=f"No chunk matched '{docref.article}'",
    )
