# 🛡️ LLM Risk Evaluation Agent
**Governance-Grade Financial Integrity Risk Classification System**

![Python](https://img.shields.io/badge/Python-3.12-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-Cloud-red) ![Anthropic](https://img.shields.io/badge/LLM-Claude%20Haiku-orange) ![Docker](https://img.shields.io/badge/Docker-Ready-blue)

Production-grade LLM evaluation system combining structured policy governance, versioned prompt engineering, and drift monitoring for financial integrity risk classification.

**🔗 Live Demo:** [llm-risk-agent.streamlit.app](https://llm-risk-agent.streamlit.app)

Built in 8 days • 300 gold cases • 150 drift cases • 3 prompt versions • 6 violation categories

---

## 🎯 What This Project Proves

✅ **Policy-driven architecture** — Taxonomy governance separated from inference engine  
✅ **Prompt versioning** — Three versions with measurable recall differences on drift  
✅ **Drift robustness** — v3 achieves zero high-severity FN on adversarial language patterns  
✅ **Production thinking** — Fail-safe defaults, audit logging, deterministic inference  
✅ **Trust & Safety alignment** — Recall prioritized over precision for safety-critical systems  

---

## 📐 Architecture
```
An interactive system diagram is available in the Streamlit dashboard under the **Architecture** tab and as `architecture/architecture.html` in this repository.

This layered design separates governance, prompt logic, inference, evaluation, and observability into clearly defined system boundaries.

Policy Layer (governance)
  └── reason_codes.json      — machine-readable violation taxonomy (v1.0)
  └── policy.md              — human-readable governance framework
  └── severity_rubric.md     — enforcement decision logic + edge cases

Prompt Layer (versioned)
  └── v1_baseline            — flat classification
  └── v2_hierarchical        — structured step-by-step reasoning
  └── v3_high_recall         — recall-optimized, implicit signal detection

Agent Layer (inference)
  └── src/llm_client.py      — provider-flexible wrapper (Anthropic/OpenAI)
  └── src/prompt_builder.py  — generic template loader
  └── src/agent.py           — classification engine, fail-safe fallback

Evaluation Layer (metrics)
  └── src/evaluator.py       — batch evaluation, per-case results
  └── src/metrics_logger.py  — persistent audit log (timestamp, model, provider)

Dashboard Layer (observability)
  └── app.py                 — 5-tab Streamlit dashboard
```

---

## 📊 Key Results

### Gold Dataset (300 cases — clean language)

| Version | Precision | Recall | F1 | HS Recall | Parse Errors |
|---|---|---|---|---|---|
| v1_baseline | 1.000 | 0.950 | 0.974 | 1.000 | 0 |
| **v2_hierarchical** | **1.000** | **0.967** | **0.983** | **1.000** | 0 |
| v3_high_recall | 1.000 | 0.950 | 0.974 | 1.000 | 0 |

All prompt versions achieve zero high-severity false negatives on clean data.  
**v2_hierarchical** delivers the highest overall recall and F1 on the gold dataset.

### Drift Dataset (150 cases — adversarial language patterns)

| Version | Recall | F1 | HS Recall | HS FN Count | Recall Drop |
|---|---|---|---|---|---|
| v1_baseline | 0.600 | 0.750 | 0.700 | 36 | 0.350 |
| v2_hierarchical | 0.800 | 0.889 | 0.950 | 6 | 0.167 |
| **v3_high_recall** | **0.840** | **0.913** | **1.000** | **0** | **0.104** |

**Key Finding:**  
On clean data, all versions perform strongly with minimal variance. Under adversarial drift, performance diverges materially — v1 misses 36 high-severity violations while v3 misses zero. This demonstrates that structured, recall-biased prompt engineering materially improves safety robustness under real-world language mutation.

---

## 🗂️ Five-Level Taxonomy

| Level | Element | Example |
|---|---|---|
| 1 | Domain | Financial Integrity |
| 2 | Category | Investment Scam |
| 3 | Violation | Guaranteed Return |
| 4 | Severity | High |
| 5 | Enforcement | Remove |

**6 categories — 11 violation patterns — 3 severity levels — 3 enforcement actions**

| Category | Violations |
|---|---|
| Investment Scam | GUARANTEED_RETURN, URGENCY_PRESSURE, FAKE_PROFIT_EVIDENCE |
| Impersonation Scam | CELEBRITY_IMPERSONATION, FAKE_INSTITUTION |
| Contact Redirection | OFF_PLATFORM_MOVE |
| Crypto Pump & Dump | PUMP_SIGNAL, UNDISCLOSED_PROMOTION |
| Loan Fraud | FAKE_LOAN_OFFER |
| Job Offer Scam | FAKE_JOB_OFFER, MONEY_MULE_RECRUITMENT |

---

## 🧪 Datasets

| Dataset | Cases | Composition |
|---|---|---|
| Gold | 300 | 60% violations (180), 40% benign (120) |
| Drift | 150 | 5 drift types × 30 cases each |

**Drift types:**
- **Slang Mutation** — Gen-Z phrasing ("no cap", "fr fr", "bussin")
- **Emoji Obfuscation** — Character substitution (G🔒uaranteed, r3turns)
- **Indirect Phrasing** — Implicit guaranteed return claims
- **Encoded Language** — Coordinated pump signals without explicit keywords
- **Subtle Medium Drift** — Off-platform redirection without platform names

---

## 🛠️ Technical Highlights

### 1. Fail Safe, Not Fail Open
```python
# Parse errors escalate — never silently allow
PARSE_ERROR_DEFAULT = {
    "label": 1,
    "violation": "PARSE_ERROR",
    "severity": "medium",
    "enforcement": "escalate_review",
    "rationale": "Model output parsing failed — escalated for safety."
}
```

### 2. Provider-Flexible LLM Client
```python
# Switch providers by changing one environment variable
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "anthropic")
LLM_MODEL = os.getenv("LLM_MODEL", "claude-haiku-4-5-20251001")
```

### 3. Retry with Exponential Backoff
```python
# Handles API overload gracefully
if any(term in str(e).lower() for term in ["overloaded", "rate", "429", "529"]):
    wait_time = 2 ** attempt
    time.sleep(wait_time)
```

### 4. Recall-Biased Prompt Design
```
PRIMARY OBJECTIVE:
When uncertain between allow and escalate_review → choose escalate_review.
When uncertain between medium and high → choose high.
```

---

## 🔧 Key Engineering Decisions

| Challenge | Decision | Rationale |
|---|---|---|
| LLM output hallucinating violation codes | Explicit enum constraints in all prompts | Prevents downstream schema mismatch |
| Parse failure defaulting to benign | Sentinel key `_parse_error` → escalate | Fail safe in safety systems |
| API overload on 900 sequential calls | Exponential backoff + 300ms throttle | Production-style resilience |
| `.format()` crashing on JSON examples | Escape curly braces as `{{}}` | Python string formatting edge case |
| Drift recall collapsing on v1 | Implicit signal detection in v3 | Slang/emoji bypass flat keyword matching |

---

## 📈 Trade-offs & Limitations

**What's Strong**  
✅ Zero high-severity FN on drift (v3)  
✅ Clean policy/prompt separation  
✅ Audit-ready evaluation logs  
✅ Production-safe failure defaults  
✅ Deterministic inference (temperature=0)  

**Production Considerations**  
❌ Synthetic dataset — real-world performance will differ  
❌ English-language only — no multilingual support  
❌ No adversarial defense mechanisms  
❌ Single domain — multi-domain extension not implemented  
❌ Static prompts — no online prompt tuning  

---

## 🎤 Talking Points

**"Walk me through your project"**  
"I built a financial integrity risk evaluation system that classifies user-generated content for scam and fraud signals. The key design decision was separating the policy layer from the inference engine — violation definitions, severity logic, and enforcement rules are all governed independently from the prompts. I then built three prompt versions with increasing recall bias and evaluated them on both clean and adversarial drift data. v1 missed 36 high-severity violations on drift. v3 missed zero."

**"Why recall over precision?"**  
"In safety systems, the cost of a false negative — missing a real violation — is much higher than a false positive. A missed money mule recruitment post could result in real financial harm to users. A false positive results in an unnecessary escalation review. The asymmetry is clear, so recall is the primary metric."

**"How would you extend this to production?"**  
"Four things: (1) Replace synthetic data with human-labeled production samples, (2) Add a confidence threshold to route borderline cases to human review queues, (3) Build a feedback loop where reviewer decisions update the gold dataset, and (4) Add multilingual support as language drift is much more severe across languages."

**"What was your biggest challenge?"**  
"v1 used `.format()` to inject content into prompt templates. The JSON output schema inside the prompt — with its curly braces — was being interpreted as Python format variables. It crashed silently and took a full debugging session to find. The fix was escaping all JSON examples in prompt files with double braces. It reinforced that prompt files are code artifacts and need the same rigor."

---

## 🗓️ Project Timeline

| Day | Focus | Deliverables |
|---|---|---|
| 1 | Foundation | Repo scaffold, config, schema, Streamlit placeholder |
| 2 | Policy & Taxonomy | reason_codes.json, policy.md, severity_rubric.md |
| 3 | Dataset Construction | 300 gold cases, 150 drift cases, validation assertions |
| 4 | Prompt Engineering | v1/v2/v3 prompts, LLM client, agent wiring |
| 5 | Evaluation Engine | Batch evaluator, metrics logger, full gold eval |
| 6 | Drift Evaluation | Drift eval, gold vs drift comparison, recall drop analysis |
| 7 | Dashboard | 4-tab Streamlit — metrics, drift monitor, taxonomy, live tester |
| 8 | README & Pipeline | Documentation, Dockerfile, clean run_pipeline.ipynb |

---

## 🗂️ Project Structure
```
LLM-risk-agent/
├── app.py                    # Streamlit dashboard
├── config.py                 # Environment-controlled settings
├── requirements.txt
├── Dockerfile                # Container deployment
├── .dockerignore
├── architecture/
│   └── architecture.html     # Interactive production architecture diagram
├── policy/
│   ├── policy.md
│   ├── reason_codes.json
│   └── severity_rubric.md
├── prompts/
│   ├── v1_baseline.txt
│   ├── v2_hierarchical.txt
│   └── v3_high_recall.txt
├── data/
│   ├── gold_cases.jsonl
│   └── drift_cases.jsonl
├── src/
│   ├── schema.py
│   ├── llm_client.py
│   ├── prompt_builder.py
│   ├── agent.py
│   ├── evaluator.py
│   └── metrics_logger.py
├── logs/
│   └── eval_runs/
│       └── eval_log.jsonl
└── .streamlit/
    └── secrets.toml.example
```

---

## 🚀 How to Run Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export ANTHROPIC_API_KEY=your-key-here

# Launch dashboard
streamlit run app.py
```

---

## 🐳 Docker Deployment
```bash
# Build image
docker build -t llm-risk-agent .

# Run container
docker run -p 8501:8501 \
  -e ANTHROPIC_API_KEY=your-key-here \
  -e LLM_PROVIDER=anthropic \
  -e LLM_MODEL=claude-haiku-4-5-20251001 \
  llm-risk-agent
```

Then open: http://localhost:8501

---

## ⚙️ Environment Variables

| Variable | Description |
|---|---|
| LLM_PROVIDER | `anthropic` or `openai` |
| LLM_MODEL | model identifier string |
| ANTHROPIC_API_KEY | required if provider=anthropic |
| OPENAI_API_KEY | required if provider=openai |

---

## 🔗 Additional Resources

- [Live Dashboard](https://llm-risk-agent.streamlit.app) — Interactive metrics and live tester
- [Policy Framework](policy/policy.md) — Governance documentation
- [Severity Rubric](policy/severity_rubric.md) — Enforcement decision logic
- [Evaluation Log](logs/eval_runs/eval_log.jsonl) — Full audit trail

---

## 📝 License

© 2026 SiDO Strategies. All rights reserved.

This repository is provided for portfolio and evaluation purposes only.  
No part of this software may be copied, modified, distributed, sublicensed, or used for commercial purposes without prior written permission from SiDO Strategies.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED.

Built by SWK • Feb 2026 • Platform Integrity & Risk Lead | MSc AI/ML (Distinction)  
[SiDO Strategies](https://sidosg.com) — AI Governance & Risk Advisory
