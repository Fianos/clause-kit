import json
import pytest
from unittest.mock import MagicMock
from src.extract import extract_rules_from_chunk
from src.schema import Rule

SAMPLE_CHUNK = {
    "article_id": "article-5",
    "article_label": "Article 5",
    "text": "Article 5\n1. The following AI practices are prohibited:\n(h) real-time biometric identification in publicly accessible spaces.",
}

DEFINITIONS = "high-risk AI system: a system listed in Annex III."

MOCK_RULES = [
    {
        "rule_id": "eu-art5-1h",
        "label": "Real-time biometric identification in public spaces",
        "condition": {"and": [{"==": [{"var": "real_time_biometric"}, True]}, {"==": [{"var": "publicly_accessible_spaces"}, True]}]},
        "obligation": "Prohibited under Article 5(1)(h)",
        "scope": "Providers and deployers",
        "exceptions": ["Victim search", "Terrorism prevention"],
        "codifiability": "high",
        "docref": {
            "source_doc": "EU AI Act (Regulation (EU) 2024/1689)",
            "article": "Article 5",
            "section": "1(h)",
            "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689#art_5",
        },
    }
]


def test_extract_returns_list_of_rules():
    mock_client = MagicMock()
    mock_client.messages.create.return_value = MagicMock(
        content=[MagicMock(text=json.dumps(MOCK_RULES))]
    )
    rules = extract_rules_from_chunk(SAMPLE_CHUNK, DEFINITIONS, domain="eu-ai-act", client=mock_client)
    assert len(rules) == 1
    assert isinstance(rules[0], Rule)
    assert rules[0].rule_id == "eu-art5-1h"
    assert rules[0].codifiability == "high"


def test_extract_handles_low_codifiability():
    low_rule = MOCK_RULES[0].copy()
    low_rule["codifiability"] = "low"
    low_rule["condition"] = None
    mock_client = MagicMock()
    mock_client.messages.create.return_value = MagicMock(
        content=[MagicMock(text=json.dumps([low_rule]))]
    )
    rules = extract_rules_from_chunk(SAMPLE_CHUNK, DEFINITIONS, domain="eu-ai-act", client=mock_client)
    assert rules[0].condition is None
    assert rules[0].codifiability == "low"


def test_extract_strips_markdown_fences():
    fenced = f"```json\n{json.dumps(MOCK_RULES)}\n```"
    mock_client = MagicMock()
    mock_client.messages.create.return_value = MagicMock(
        content=[MagicMock(text=fenced)]
    )
    rules = extract_rules_from_chunk(SAMPLE_CHUNK, DEFINITIONS, domain="eu-ai-act", client=mock_client)
    assert len(rules) == 1
