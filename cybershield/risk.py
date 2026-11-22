"""
Deterministic defensive risk scoring.
Scores indicate review priority, NOT probability of compromise.
"""

def assess_rows(rows):
    assessments = []
    label_weights = {"normal": 10, "suspicious": 45, "anomaly": 60}

    for row in rows:
        label = str(row.get("label", "normal")).strip().lower()
        try:
            count = max(0, int(row.get("count", 0)))
        except (ValueError, TypeError):
            count = 0

        base_score = label_weights.get(label, 10)

        # Volume bonus applies only to suspicious/anomalous events.
        count_bonus = 0
        if label in ("suspicious", "anomaly"):
            if count >= 40:
                count_bonus = 25
            elif count >= 30:
                count_bonus = 20
            elif count >= 20:
                count_bonus = 15
            elif count >= 10:
                count_bonus = 10

        score = min(100, base_score + count_bonus)
        severity = "HIGH" if score >= 80 else "MEDIUM" if score >= 50 else "LOW"

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

    return sorted(assessments, key=lambda item: item["risk_score"], reverse=True)
