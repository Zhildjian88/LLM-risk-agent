# Financial Integrity Risk Policy
**Version:** 1.0
**Last Updated:** 2026-02-19
**Owner:** Risk Strategy
**Review Cycle:** 30 days

---

## 1. Purpose
This policy defines violation standards for financial integrity risk content.
It governs how the evaluation agent classifies, scores, and recommends
enforcement actions for content promoting financial fraud or scams.

---

## 2. Scope
Content is in scope if it involves:
- Financial products, investments, or returns
- Employment or income opportunities
- Crypto assets or trading signals
- Loan or credit offers
- Instructions to contact external parties for financial purposes

---

## 3. Categories & Violations

| Category | Violation Code | Severity | Enforcement |
|---|---|---|---|
| Investment Scam | GUARANTEED_RETURN | High | Remove |
| Investment Scam | URGENCY_PRESSURE | Medium | Escalate Review |
| Investment Scam | FAKE_PROFIT_EVIDENCE | High | Remove |
| Impersonation Scam | CELEBRITY_IMPERSONATION | High | Remove |
| Impersonation Scam | FAKE_INSTITUTION | High | Remove |
| Contact Redirection | OFF_PLATFORM_MOVE | Medium | Escalate Review |
| Crypto Pump & Dump | PUMP_SIGNAL | High | Remove |
| Crypto Pump & Dump | UNDISCLOSED_PROMOTION | Medium | Escalate Review |
| Loan Fraud | FAKE_LOAN_OFFER | High | Remove |
| Job Offer Scam | FAKE_JOB_OFFER | High | Remove |
| Job Offer Scam | MONEY_MULE_RECRUITMENT | High | Remove |

---

## 4. Severity Definitions

| Severity | Definition | Risk Weight |
|---|---|---|
| High | Clear violation with direct harm potential. Immediate action warranted. | 3 |
| Medium | Probable violation or strong signal. Human review recommended. | 2 |
| Low | Weak or ambiguous signal. Monitor only. | 1 |

---

## 5. Enforcement Actions

| Action | Trigger Condition |
|---|---|
| remove | High severity, unambiguous violation |
| escalate_review | Medium severity or ambiguous high severity |
| allow | No violation detected |

---

## 6. Ambiguity Rules
The following content is NOT a violation:
- Educational content about scam awareness
- News reporting on financial fraud
- Satire clearly marked as such
- General financial discussion without violation signals

When ambiguity exists between two severity levels:
- Default to the higher severity
- Default action: escalate_review, never allow under uncertainty

---

## 7. Escalation Rules
Escalate to senior review when:
- Content involves a named public figure
- Content is borderline between medium and high
- Content involves a novel or emerging scam pattern
- Model output is inconsistent across prompt versions

---

## 8. Operational Metrics
The effectiveness of this policy is measured using:

- Overall Precision, Recall, and F1 score
- High-Severity Recall (primary safety metric)
- High-Severity False Negative Count (critical risk metric)
- Drift Recall on emerging language patterns
- Latency (p50 and p95) for online feasibility

High-severity recall is prioritized over overall precision due to potential user harm.

---

## 9. Policy Extensibility
This taxonomy is structured for extensibility.
Categories and violation patterns can be:
- Extended to additional risk domains (e.g. Hate Speech, Misinformation)
- Adapted to platform-specific policy frameworks
- Updated as new violation patterns emerge

The policy layer is intentionally separated from the evaluation engine.
Policy changes do not require modification of the classification pipeline.
