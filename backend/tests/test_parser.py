from pathlib import Path

from app.parsers.markdown_parser import parse_markdown_file
from app.parsers.normalizer import normalize_parsed_file


def test_parse_current_sample() -> None:
    parsed = parse_markdown_file(Path("unit_1_1/part1.md"))
    assert parsed.unit_id == "unit_1_1"
    assert len(parsed.items) >= 1

    normalized = normalize_parsed_file(parsed)
    assert normalized[0].answers == ["소프트웨어 생명 주기"]
