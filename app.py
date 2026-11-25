from pathlib import Path
import streamlit as st
import pandas as pd

from logtriage.workflow import run
from logtriage.report import create_pdf

st.set_page_config(
    page_title="LogTriage Agents",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ LogTriage Agents")
st.caption("Local multi-agent defensive cyber threat intelligence research lab")

st.warning(
    "Defensive research prototype only. Use synthetic or explicitly "
    "authorized sanitized logs. No live network scanning or offensive actions. "
    "Never paste passwords, secrets, or sensitive infrastructure data."
)

demo = Path(__file__).parent / "data" / "synthetic_defensive_logs.csv"

if "logs" not in st.session_state:
    st.session_state.logs = ""
if "advisory" not in st.session_state:
    st.session_state.advisory = ""
if "question" not in st.session_state:
    st.session_state.question = (
        "Which synthetic log events merit defensive analyst review, "
        "and what benign explanations or evidence gaps should be considered?"
    )

if st.button("Load Synthetic Lab Logs"):
    st.session_state.logs = demo.read_text(encoding="utf-8")
    st.rerun()

st.subheader("Research configuration")

question = st.text_area("Research question", key="question", height=90)
logs = st.text_area(
    "Synthetic / authorized sanitized CSV logs",
    key="logs",
    height=240,
    help="Required columns: timestamp,asset,event,count,label"
)
advisory = st.text_area(
    "Optional public cyber advisory text",
    key="advisory",
    height=120
)

if st.button("Run Multi-Agent Defensive Analysis",
             type="primary", use_container_width=True):

    progress_area = st.empty()
    status = st.empty()

    try:
        def progress(stage, mdl):
            progress_area.info(f"{stage} | Model: {mdl}")

        with st.spinner("Running local AI agents..."):
            summary, results = run(
                logs, advisory, question, progress
            )

        progress_area.empty()
        status.success(
            "Analysis complete. Human analyst validation is required."
        )

        st.divider()
        st.subheader("Dataset Overview")

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Records", summary.get("records", 0))
        col2.metric(
            "Flagged Records",
            len(summary.get("flagged_rows", []))
        )
        col3.metric(
            "Event Types",
            len(summary.get("event_counts", {}))
        )

        st.subheader("Deterministic Dataset Summary")
        st.json(summary)

        assessments = summary.get("risk_assessments", [])

        if assessments:
            st.divider()
            st.subheader("Risk Assessment Dashboard")

            risk_df = pd.DataFrame(assessments)
            risk_df["asset_event"] = (
                risk_df["asset"].astype(str)
                + " — "
                + risk_df["event"].astype(str)
            )

            risk_chart = risk_df[["asset_event", "risk_score"]].copy()
            st.bar_chart(
                risk_chart,
                x="asset_event",
                y="risk_score",
                y_label="Review priority score (0-100)"
            )

            st.subheader("Severity Distribution")
            severity_counts = (
                risk_df["severity"]
                .value_counts()
                .reindex(["HIGH", "MEDIUM", "LOW"], fill_value=0)
                .rename_axis("Severity")
                .reset_index(name="Records")
            )
            st.bar_chart(
                severity_counts,
                x="Severity",
                y="Records",
                x_label="Severity Level",
                y_label="Number of records"
            )

            st.subheader("Risk Assessment Details")
            st.dataframe(
                risk_df[
                    ["asset", "event", "count", "risk_score", "severity"]
                ],
                use_container_width=True,
                hide_index=True
            )

            st.caption(
                "Scores represent deterministic defensive review priority, "
                "not probability of compromise."
            )

        st.divider()
        st.subheader("Multi-Agent Research Results")

        for heading, body in results.items():
            is_final = heading == "Coordinator - Final Report"
            with st.expander(heading, expanded=is_final):
                st.markdown(body)

        report = [
            "# LogTriage Agents - Defensive Research Report",
            "\n## Deterministic Summary",
            "```json",
            __import__("json").dumps(summary, indent=2),
            "```"
        ]

        for heading, body in results.items():
            report.extend([f"\n## {heading}", body])

        st.download_button(
            "Download Complete Markdown Report",
            "\n\n".join(report),
            "logtriage_defensive_report.md",
            "text/markdown",
            use_container_width=True
        )

        pdf_bytes = create_pdf(summary, results)

        st.download_button(
            "Download PDF Research Report",
            pdf_bytes,
            "logtriage_defensive_report.pdf",
            "application/pdf",
            use_container_width=True
        )

    except Exception as error:
        progress_area.empty()
        status.error(f"Analysis failed: {error}")

st.divider()
st.caption(
    "LogTriage Agents | Local AI research | "
    "Synthetic and authorized defensive data only"
)
