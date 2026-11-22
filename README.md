# CyberShield WarAI
**Local multi-agent defensive cyber threat intelligence and critical-infrastructure resilience research lab.**

This prototype analyzes researcher-provided public cyber advisories and synthetic defensive security logs. It classifies observations, flags possible anomalies for human review, and drafts a defensive incident report.

## Safety boundary
This is strictly defensive. It does not scan networks, exploit systems, write malware, evade detection, steal credentials, or provide offensive instructions. The included logs are synthetic. Do not paste secrets, personal data, production logs, or sensitive infrastructure details.

## Requirements
- macOS, Python 3.10+
- Ollama running locally
- Models: `qwen2.5:7b`, `llama3.1:8b`, `mistral:7b`, `qwen2.5:3b`, `llama3.2:3b`

## Run
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
ollama list
streamlit run app.py
```
If needed, start Ollama separately with `ollama serve`. Open the local Streamlit URL, usually http://localhost:8501.

## Demo
Click **Load synthetic lab logs** and **Run defensive analysis**. The dataset is invented and not connected to a real network.

## Research evaluation
Compare a rules-only baseline, a single-LLM baseline, and the multi-agent pipeline. Measure anomaly precision/recall against synthetic labels, false-positive rate, explanation quality, evidence traceability, reviewer correction rate, latency, and local memory use. This is not a production IDS.
