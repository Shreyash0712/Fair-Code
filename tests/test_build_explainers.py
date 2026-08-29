import importlib


def test_parse_table_accepts_two_dash_separator_row():
    # explainers/false-positives-vs-false-negatives.md's real separator row
    # is |--|--|--| (2 dashes/cell) - valid GFM, but this parser used to
    # require 3+ dashes and would silently fall through to garbled
    # plain-text lines instead of a real <table> (#324).
    script = importlib.import_module("scripts.build_explainers")
    lines = [
        "| | False Positive | False Negative |",
        "|--|--|--|",
        "| What happens | flags risk | says low risk |",
    ]

    result = script.parse_table(lines, 0)

    assert result is not None
    headers, body_rows, next_index = result
    assert headers == ["", "False Positive", "False Negative"]
    assert body_rows == [["What happens", "flags risk", "says low risk"]]


def test_parse_table_still_accepts_three_dash_separator_row():
    script = importlib.import_module("scripts.build_explainers")
    lines = [
        "| A | B |",
        "|---|---|",
        "| 1 | 2 |",
    ]

    result = script.parse_table(lines, 0)

    assert result is not None
    headers, _body_rows, _next_index = result
    assert headers == ["A", "B"]
