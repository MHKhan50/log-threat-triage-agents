from logtriage.risk import assess_rows


def test_anomaly_high_count_gets_high_priority():
    rows = [{
        "timestamp": "2026-09-10T09:20:00Z",
        "asset": "LAB-WEB-01",
        "event": "failed_login",
        "count": 48,
        "label": "anomaly",
    }]

    result = assess_rows(rows)

    assert result[0]["risk_score"] == 85
    assert result[0]["severity"] == "HIGH"


def test_suspicious_event_gets_deterministic_score():
    rows = [{
        "timestamp": "2026-09-10T09:25:00Z",
        "asset": "LAB-FILE-01",
        "event": "large_file_read",
        "count": 37,
        "label": "suspicious",
    }]

    first = assess_rows(rows)
    second = assess_rows(rows)

    assert first == second
    assert first[0]["risk_score"] == 65
    assert first[0]["severity"] == "MEDIUM"


def test_normal_low_count_is_low_priority():
    rows = [{
        "timestamp": "2026-09-10T09:00:00Z",
        "asset": "LAB-01",
        "event": "successful_login",
        "count": 2,
        "label": "normal",
    }]

    result = assess_rows(rows)

    assert result[0]["risk_score"] == 10
    assert result[0]["severity"] == "LOW"
