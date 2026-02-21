"""
app.py — LLM Risk Evaluation Agent Dashboard
Day 7: Full dashboard with metrics, drift monitoring, and live tester.
"""

import streamlit as st
import pandas as pd
import json
import config
from pathlib import Path

st.set_page_config(
    page_title="LLM Risk Evaluation Agent",
    page_icon="🛡️",
    layout="wide"
)

# ── Helpers ───────────────────────────────────────────────────────────────
def load_eval_log():
    log_path = Path("logs/eval_runs/eval_log.jsonl")
    if not log_path.exists():
        return pd.DataFrame()
    rows = [json.loads(l) for l in log_path.read_text().strip().splitlines()]
    return pd.DataFrame(rows)

def load_taxonomy():
    with open("policy/reason_codes.json") as f:
        return json.load(f)

# ── Header ────────────────────────────────────────────────────────────────
st.title("🛡️ LLM Risk Evaluation Agent")
st.caption("Financial Integrity | Structured Risk Taxonomy | Prompt Versioning | Drift Monitoring")
st.markdown(
    f"**Provider:** `{config.LLM_PROVIDER}` | "
    f"**Model:** `{config.LLM_MODEL}`"
)

# ── Tabs ──────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Metrics Dashboard",
    "🌊 Drift Monitor",
    "🗂️ Taxonomy",
    "🔍 Live Tester",
    "🏗️ Architecture"
])

# ── Tab 1: Metrics Dashboard ──────────────────────────────────────────────
with tab1:
    st.header("Prompt Version Comparison")
    df = load_eval_log()

    if df.empty:
        st.warning("No evaluation runs found.")
    else:
        gold_df = df[df["dataset"] == "gold"].copy()
        if not gold_df.empty:
            st.subheader("Gold Dataset Results")
            display_cols = ["prompt_version", "precision", "recall", "f1",
                          "high_severity_recall", "high_severity_fn_count",
                          "parse_error_count", "p50_latency_ms", "p95_latency_ms"]
            latest_gold = (
                gold_df.sort_values("timestamp")
                       .groupby("prompt_version")
                       .last()
                       .reset_index()
            )
            st.dataframe(latest_gold[display_cols], use_container_width=True)

            col1, col2, col3 = st.columns(3)
            best = latest_gold.loc[latest_gold["recall"].idxmax()]
            col1.metric("Best Recall", f"{best['recall']:.3f}", best["prompt_version"])
            best_hs = latest_gold.loc[latest_gold["high_severity_recall"].idxmax()]
            col2.metric("Best HS Recall", f"{best_hs['high_severity_recall']:.3f}", best_hs["prompt_version"])
            lowest_fn = latest_gold.loc[latest_gold["high_severity_fn_count"].idxmin()]
            col3.metric("Lowest HS FN", int(lowest_fn["high_severity_fn_count"]), lowest_fn["prompt_version"])

# ── Tab 2: Drift Monitor ──────────────────────────────────────────────────
with tab2:
    st.header("Drift Recall Monitor")
    df = load_eval_log()

    if df.empty:
        st.warning("No evaluation runs found.")
    else:
        gold_df = df[df["dataset"] == "gold"][["prompt_version", "recall", "high_severity_recall", "timestamp"]].copy()
        drift_df = df[df["dataset"] == "drift"][["prompt_version", "recall", "high_severity_recall", "timestamp"]].copy()

        if not gold_df.empty and not drift_df.empty:
            gold_latest = (
                gold_df.sort_values("timestamp")
                       .groupby("prompt_version")
                       .last()
                       .reset_index()
            )
            drift_latest = (
                drift_df.sort_values("timestamp")
                        .groupby("prompt_version")
                        .last()
                        .reset_index()
            )

            merged = gold_latest.merge(drift_latest, on="prompt_version", suffixes=("_gold", "_drift"))
            merged["recall_drop"] = (merged["recall_gold"] - merged["recall_drift"]).round(3)
            merged["hs_recall_drop"] = (merged["high_severity_recall_gold"] - merged["high_severity_recall_drift"]).round(3)

            st.subheader("Gold vs Drift Recall")
            st.dataframe(merged[[
                "prompt_version",
                "recall_gold", "recall_drift", "recall_drop",
                "high_severity_recall_gold", "high_severity_recall_drift", "hs_recall_drop"
            ]], use_container_width=True)

            st.subheader("Recall Drop by Version")
            st.bar_chart(merged.set_index("prompt_version")["recall_drop"])

            st.subheader("High-Severity Recall Drop by Version")
            st.bar_chart(merged.set_index("prompt_version")["hs_recall_drop"])

            st.info("✅ v3_high_recall achieves zero high-severity FN on drift — recommended for production.")

# ── Tab 3: Taxonomy ───────────────────────────────────────────────────────
with tab3:
    st.header("Financial Integrity Risk Taxonomy")
    taxonomy = load_taxonomy()

    st.markdown(f"**Version:** {taxonomy.get('version')} | "
                f"**Owner:** {taxonomy.get('owner')} | "
                f"**Review Cycle:** {taxonomy.get('review_cycle_days')} days")

    rows = []
    for cat in taxonomy["categories"]:
        for v in cat["violations"]:
            rows.append({
                "Category": cat["label"],
                "Violation Code": v["code"],
                "Severity": v["severity"].upper(),
                "Risk Weight": v["risk_weight"],
                "Enforcement": v["enforcement"],
                "Description": v["description"]
            })

    tax_df = pd.DataFrame(rows)
    severity_filter = st.multiselect(
        "Filter by Severity",
        options=["HIGH", "MEDIUM", "LOW"],
        default=["HIGH", "MEDIUM", "LOW"]
    )
    filtered = tax_df[tax_df["Severity"].isin(severity_filter)]
    st.dataframe(filtered, use_container_width=True)

# ── Tab 4: Live Tester ────────────────────────────────────────────────────
with tab4:
    st.header("Live Content Tester")
    st.caption("Classify content in real time using any prompt version.")

    provider = config.LLM_PROVIDER
    api_key = st.text_input(f"{provider.upper()} API Key", type="password")
    prompt_version = st.selectbox(
        "Prompt Version",
        ["v1_baseline", "v2_hierarchical", "v3_high_recall"]
    )
    text_input = st.text_area("Content to evaluate", height=120)

    if st.button("🔍 Classify"):
        if not api_key:
            st.error("Please enter your API key.")
        elif not text_input.strip():
            st.error("Please enter content to evaluate.")
        else:
            import os, sys
            if provider == "anthropic":
                os.environ["ANTHROPIC_API_KEY"] = api_key
            elif provider == "openai":
                os.environ["OPENAI_API_KEY"] = api_key
            sys.path.insert(0, ".")
            with st.spinner("Classifying..."):
                try:
                    from src.agent import Agent
                    agent = Agent(prompt_version=prompt_version)
                    result = agent.classify(text_input)
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Label", "🚨 Violation" if result.label == 1 else "✅ Benign")
                    col2.metric("Severity", result.severity.upper())
                    col3.metric("Enforcement", result.enforcement)
                    st.markdown(f"**Violation:** `{result.violation}`")
                    st.markdown(f"**Category:** `{result.category}`")
                    st.markdown(f"**Rationale:** {result.rationale}")
                    st.markdown(f"**Latency:** {result.latency_ms}ms")
                except Exception as e:
                    st.error(f"Error: {e}")

# ── Tab 5: Architecture ───────────────────────────────────────────────────
with tab5:
    st.header("Production Architecture")

    arch_path = Path("architecture/architecture.html")

    if arch_path.exists():
        html_content = arch_path.read_text()
        st.components.v1.html(html_content, height=1200, scrolling=True)
    else:
        st.warning("architecture.html not found.")
        
