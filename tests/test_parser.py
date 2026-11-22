from pathlib import Path
from cybershield.log_parser import parse_csv, rules_summary

def test_synthetic_dataset_parses():
    raw = (Path(__file__).parents[1] / "data" / "synthetic_defensive_logs.csv").read_text()
    rows = parse_csv(raw)
    assert len(rows) == 10
    assert len(rules_summary(rows)["flagged_rows"]) == 2

def test_missing_columns_rejected():
    try:
        parse_csv("timestamp,asset\nnow,host")
    except ValueError as e:
        assert "columns" in str(e)
    else:
        assert False, "Expected validation error"
