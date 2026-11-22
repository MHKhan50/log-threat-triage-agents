import json
import textwrap
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Preformatted, PageBreak
)


def create_pdf(summary, results):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title="CyberShield WarAI Defensive Research Report"
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="ReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        textColor=colors.HexColor("#17365D"),
        spaceAfter=18
    ))

    styles.add(ParagraphStyle(
        name="AgentHeading",
        parent=styles["Heading2"],
        textColor=colors.HexColor("#17365D"),
        spaceBefore=14,
        spaceAfter=8
    ))

    styles.add(ParagraphStyle(
        name="ReportBody",
        parent=styles["BodyText"],
        leading=14,
        spaceAfter=7
    ))

    story = [
        Paragraph("CyberShield WarAI", styles["ReportTitle"]),
        Paragraph(
            "Defensive Cybersecurity Research Report",
            styles["Heading2"]
        ),
        Spacer(1, 10),
        Paragraph(
            "Research prototype. Findings require human validation. "
            "Based on synthetic or explicitly authorized sanitized data.",
            styles["Italic"]
        ),
        Spacer(1, 12),
        Paragraph("Deterministic Dataset Summary", styles["Heading1"])
    ]

    summary_text = json.dumps(summary, indent=2, ensure_ascii=False)
    wrapped_summary = "\n".join(
        textwrap.fill(line, width=88) if len(line) > 88 else line
        for line in summary_text.splitlines()
    )
    story.append(Preformatted(
        wrapped_summary,
        ParagraphStyle(
            "SummaryCode",
            fontName="Courier",
            fontSize=7,
            leading=9
        )
    ))

    for heading, body in results.items():
        story.append(Paragraph(heading, styles["AgentHeading"]))

        for paragraph in str(body).split("\n\n"):
            if paragraph.strip():
                safe_text = (
                    paragraph.replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
                    .replace("\n", "<br/>")
                )
                story.append(Paragraph(safe_text, styles["ReportBody"]))

    doc.build(story)
    return buffer.getvalue()
