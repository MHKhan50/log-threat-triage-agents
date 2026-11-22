# Paper outline: CyberShield WarAI

## Proposed title
CyberShield WarAI: A Local Multi-Agent LLM Framework for Defensive Cyber Threat Intelligence and Critical-Infrastructure Resilience

## Research question
Can multi-agent critique improve the quality and explainability of defensive triage on synthetic cyber telemetry compared with rules-only and single-LLM baselines?

## Sections
1. Introduction and motivation
2. Related work: defensive cyber threat intelligence, anomaly detection, LLM-based SOC assistance
3. System architecture and local inference
4. Synthetic dataset generation and labels
5. Experimental baselines: deterministic rules, single LLM, multi-agent without reviewer, full pipeline
6. Metrics: precision/recall, false-positive rate, evidence citation accuracy, unsupported-claim rate, analyst rubric, latency
7. Results with measured values and error analysis
8. Discussion: local deployment, model limitations, human analyst role
9. Safety, ethics, reproducibility, limitations
10. Conclusion

The bundled CSV is only a toy demo. It is not a validated benchmark or a real intrusion dataset. Never claim production detection performance based on it.
