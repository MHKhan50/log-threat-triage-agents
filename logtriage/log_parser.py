import csv, io
from collections import Counter

REQUIRED = {"timestamp", "asset", "event", "count", "label"}

def parse_csv(raw):
    reader = csv.DictReader(io.StringIO(raw.strip()))
    if not reader.fieldnames or not REQUIRED.issubset(set(reader.fieldnames)):
        raise ValueError("CSV must include columns: timestamp, asset, event, count, label")
    rows = []
    for line, row in enumerate(reader, start=2):
        try:
            count = int(row["count"])
        except (TypeError, ValueError):
            raise ValueError(f"Invalid integer in count at CSV line {line}")
        rows.append({
            "timestamp": row["timestamp"].strip(),
            "asset": row["asset"].strip(),
            "event": row["event"].strip(),
            "count": count,
            "label": row["label"].strip().lower()
        })
    if not rows: raise ValueError("CSV contains no records.")
    return rows

def rules_summary(rows):
    counts = Counter(r["event"] for r in rows)
    flagged = [r for r in rows if r["label"] in {"anomaly", "suspicious"}]
    return {
        "records": len(rows),
        "event_counts": dict(counts),
        "synthetic_label_counts": dict(Counter(r["label"] for r in rows)),
        "flagged_rows": flagged
    }
