from pathlib import Path
import streamlit as st
from cybershield.workflow import run

st.set_page_config(page_title="CyberShield WarAI", page_icon="🛡️", layout="wide")
st.title("🛡️ CyberShield WarAI")
st.caption("Local multi-agent defensive cyber threat intelligence research lab")
st.warning("Defensive research prototype only. No network scanning or offensive actions. Use synthetic or explicitly authorized sanitized logs; never paste secrets or sensitive infrastructure data.")

demo = Path(__file__).parent / "data" / "synthetic_defensive_logs.csv"
if "logs" not in st.session_state: st.session_state.logs = ""
if "advisory" not in st.session_state: st.session_state.advisory = ""
if "question" not in st.session_state: st.session_state.question = "Which synthetic log events merit defensive analyst review, and what benign explanations or evidence gaps should be considered?"
if st.button("Load synthetic lab logs"):
    st.session_state.logs = demo.read_text(encoding="utf-8")
    st.rerun()

question = st.text_area("Research question", key="question", height=80)
logs = st.text_area("Synthetic / authorized sanitized CSV logs", key="logs", height=240,
                    help="Required columns: timestamp,asset,event,count,label")
advisory = st.text_area("Optional public cyber advisory text", key="advisory", height=140)
if st.button("Run defensive analysis", type="primary", use_container_width=True):
    status = st.empty()
    try:
        def progress(stage, mdl): status.info(f"{stage} — `{mdl}`")
        with st.spinner("Running parser and five local agents..."):
            summary, results = run(logs, advisory, question, progress)
        status.success("Analysis complete. Validate findings with a human analyst.")
        st.subheader("Deterministic CSV summary")
        st.json(summary)
        report = ["# Deterministic summary\n\n" + str(summary)]
        for heading, body in results.items():
            report.append(f"# {heading}\n\n{body}")
            with st.expander(heading, expanded=heading == "Defensive incident brief"):
                st.markdown(body)
        st.download_button("Download complete defensive report", "\n\n".join(report),
                           "cybershield_defensive_report.md", "text/markdown")
    except Exception as e: st.error(str(e))
st.divider()
st.caption("Synthetic lab dataset. This application does not connect to or inspect a live network.")
