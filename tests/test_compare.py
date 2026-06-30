import json
import pytest
from pathlib import Path
from unittest.mock import MagicMock
from src.compare import run_comparison, _strip_xml_tags, _extract_label
from src.schema import ComparisonResult

MINIMAL_AKN = """\
<?xml version="1.0" encoding="UTF-8"?>
<akomaNtoso>
  <act>
    <body>
      <section eId="sec-26WA">
        <num>26WA</num>
        <heading>Eligible data breaches</heading>
        <subsection eId="sec-26WA-subs-1">
          <num>(1)</num>
          <content>
            <p>There is an <term>eligible data breach</term> if there is unauthorised access to <term>personal information</term>.</p>
          </content>
        </subsection>
      </section>
    </body>
  </act>
</akomaNtoso>"""

MOCK_RULE = {
    "rule_id": "ndb-26wa-001",
    "label": "Eligible data breach",
    "condition": None,
    "obligation": "Notify the Commissioner and affected individuals.",
    "scope": "APP entities",
    "exceptions": [],
    "codifiability": "low",
    "docref": {
        "source_doc": "Privacy Act 1988 (Cth)",
        "article": "Section 26WA",
        "section": "26WA(1)",
        "url": "https://www.legislation.gov.au/Details/C2024C00091",
    },
}


def test_strip_xml_tags_removes_tags():
    xml = "<section><num>26WA</num><p>Some <term>text</term>.</p></section>"
    result = _strip_xml_tags(xml)
    assert "<" not in result
    assert "26WA" in result
    assert "text" in result


def test_extract_label_returns_num_and_heading():
    label = _extract_label(MINIMAL_AKN)
    assert "26WA" in label
    assert "Eligible data breaches" in label


def test_run_comparison_returns_both_rule_sets(tmp_path):
    (tmp_path / "ndb-26wa.xml").write_text(MINIMAL_AKN)
    mock_client = MagicMock()
    mock_client.messages.create.return_value = MagicMock(
        content=[MagicMock(text=json.dumps([MOCK_RULE]))]
    )

    result = run_comparison("26wa", "ndb", data_dir=tmp_path, client=mock_client)

    assert isinstance(result, ComparisonResult)
    assert result.domain == "ndb"
    assert result.section_id == "26wa"
    assert len(result.plain_rules) == 1
    assert len(result.akn_rules) == 1
    assert mock_client.messages.create.call_count == 2


def test_run_comparison_plain_path_strips_tags(tmp_path):
    (tmp_path / "ndb-26wa.xml").write_text(MINIMAL_AKN)
    mock_client = MagicMock()
    mock_client.messages.create.return_value = MagicMock(
        content=[MagicMock(text=json.dumps([MOCK_RULE]))]
    )

    run_comparison("26wa", "ndb", data_dir=tmp_path, client=mock_client)

    calls = mock_client.messages.create.call_args_list
    plain_content = calls[0].kwargs["messages"][0]["content"]
    akn_content = calls[1].kwargs["messages"][0]["content"]
    assert "<section" not in plain_content
    assert "<section" in akn_content


def test_run_comparison_missing_section_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        run_comparison("99zz", "ndb", data_dir=tmp_path, client=MagicMock())
