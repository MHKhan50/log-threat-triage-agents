"""
Deterministic defensive risk scoring.
Scores are review-priority indicators, NOT probabilities of compromise.
"""

def assess_rows(rows):
    assessments = []

    label_weights = {
        "normal": 10,
        "suspicious": 45,
        "anomaly": 60,
    }

    for row in rows:
        label = str(row.get("label", "normal")).strip().lower()

        try:
            count = max(0, int(row.get("count", 0)))
        except (ValueError, TypeError):
            count = 0

        base_score = label_weights.get(label, 10)

        if count >= 40:
            count_bonus = 25
        elif count >= 30:
            count_bonus = 20
        elif count >= 20:
            count_bonus = 15
        elif count >= 10:
            count_bonus = 10
        else:
            count_bonus = 0

        score = min(100, base_score + count_bonus)

        if score >= 80:
            severity = "HIGH"
        elif score >= 50:
            severity = "MEDIUM"
        else:
            severity = "LOW"

        assessments.append({
            "timestamp": row.get("timestamp", ""),
            "asset": row.get("asset", ""),
            "event": row.get("event", ""),
            "label": label,
            "count": count,
            "base_score": base_score,
            "count_bonus": count_bonus,
            "risk_score": score,
            "severity": severity,
            "meaning": "Defensive review priority; not a probability of compromise."
        })

    return sorted(
        assessments,
        key=lambda item: item["risk_score"],
        reverse=True
    )
