import json
from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether
)
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart


def create_pdf(summary, results):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        rightMargin=16 * mm, leftMargin=16 * mm,
        topMargin=18 * mm, bottomMargin=18 * mm,
        title="CyberShield WarAI Defensive Research Report"
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="CSCover", parent=styles["Title"],
        alignment=TA_CENTER, textColor=colors.HexColor("#17365D"),
        fontSize=25, leading=30, spaceAfter=10
    ))
    styles.add(ParagraphStyle(
        name="CSBody", parent=styles["BodyText"],
        leading=14, spaceAfter=7
    ))
    styles.add(ParagraphStyle(
        name="CSAgent", parent=styles["Heading2"],
        textColor=colors.HexColor("#17365D"),
        spaceBefore=12, spaceAfter=6
    ))

    story = [
        Spacer(1, 28 * mm),
        Paragraph("CYBERSHIELD WARAI", styles["CSCover"]),
        Paragraph("Defensive Cybersecurity Research Report",
                  styles["Heading2"]),
        Spacer(1, 8 * mm),
        Paragraph("Masmatix Innovations", styles["Heading2"]),
        Spacer(1, 8 * mm),
        Paragraph(
            "Research prototype. Findings require human validation. "
            "Use only synthetic or explicitly authorized sanitized data.",
            styles["Italic"]
        ),
        Spacer(1, 15 * mm),
        Paragraph("Executive Summary", styles["Heading1"])
    ]

    risk_rows = summary.get("risk_assessments", [])
    total = summary.get("total_records", summary.get("records", "N/A"))
    flagged = summary.get("flagged_records", summary.get("flagged", "N/A"))

    overview = [
        ["Metric", "Value"],
        ["Records analyzed", str(total)],
        ["Flagged records", str(flagged)],
        ["Risk assessments", str(len(risk_rows))]
    ]
    table = Table(overview, colWidths=[75 * mm, 75 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17365D")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#B8C4D1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#F1F5F9")]),
        ("PADDING", (0, 0), (-1, -1), 7)
    ]))
    story += [table, Spacer(1, 10), Paragraph(
        "Risk Review Summary", styles["Heading1"]
    )]

    severity_counts = {
        level: sum(1 for item in risk_rows if item.get("severity") == level)
        for level in ("HIGH", "MEDIUM", "LOW")
    }

    if risk_rows:
        drawing = Drawing(420, 175)
        chart = VerticalBarChart()
        chart.x = 45
        chart.y = 25
        chart.height = 125
        chart.width = 330
        chart.data = [[severity_counts[x] for x in ("HIGH", "MEDIUM", "LOW")]]
        chart.categoryAxis.categoryNames = ["HIGH", "MEDIUM", "LOW"]
        chart.valueAxis.valueMin = 0
        chart.valueAxis.valueMax = max(1, max(severity_counts.values()) + 1)
        chart.valueAxis.valueStep = 1
        chart.bars[0].fillColor = colors.HexColor("#2874A6")
        drawing.add(chart)
        story.append(drawing)

        risk_table = [["Asset", "Event", "Count", "Score", "Severity"]]
        for item in risk_rows[:25]:
            risk_table.append([
                str(item.get("asset", ""))[:22],
                str(item.get("event", ""))[:22],
                str(item.get("count", "")),
                str(item.get("risk_score", "")),
                str(item.get("severity", ""))
            ])
        t = Table(risk_table, repeatRows=1,
                  colWidths=[35*mm, 42*mm, 17*mm, 17*mm, 25*mm])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17365D")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#B8C4D1")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1),
             [colors.white, colors.HexColor("#F1F5F9")]),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("PADDING", (0, 0), (-1, -1), 5)
        ]))
        story += [Spacer(1, 6), t]
    else:
        story.append(Paragraph(
            "No deterministic risk assessments were supplied.",
            styles["CSBody"]
        ))

    story.append(PageBreak())
    story.append(Paragraph("Dataset Summary (JSON)", styles["Heading1"]))
    safe_json = escape(json.dumps(summary, indent=2, ensure_ascii=False))
    story.append(Paragraph(
        "<font name='Courier' size='7'>" +
        safe_json.replace("\n", "<br/>").replace(" ", "&nbsp;") +
        "</font>", styles["CSBody"]
    ))

    for heading, body in results.items():
        story.append(Paragraph(escape(str(heading)), styles["CSAgent"]))
        for paragraph in str(body).split("\n\n"):
            if paragraph.strip():
                safe = escape(paragraph).replace("\n", "<br/>")
                story.append(Paragraph(safe, styles["CSBody"]))

    def footer(canvas, document):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#64748B"))
        canvas.drawString(16 * mm, 10 * mm, "CyberShield WarAI | Human validation required")
        canvas.drawRightString(A4[0] - 16 * mm, 10 * mm,
                               f"Page {document.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    return buffer.getvalue()
