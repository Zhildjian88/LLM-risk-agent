# Severity Rubric — Financial Integrity
**Version:** 1.0
**Last Updated:** 2026-02-19
**Owner:** Risk Strategy

---

## HIGH (Risk Weight: 3) → remove

Assign HIGH when content contains ONE OR MORE of:
- Explicit guaranteed or risk-free return claim
- Direct impersonation of celebrity, regulator, or institution
- Upfront fee requirement for loan or job offer
- Coordinated crypto pump signal with urgency
- Money mule recruitment language
- Fabricated profit screenshots or unverifiable return claims

**Default action:** remove
**Review requirement:** None — automated removal warranted (subject to periodic audit sampling)

---

## MEDIUM (Risk Weight: 2) → escalate_review

Assign MEDIUM when content contains:
- Urgency or scarcity pressure without explicit guarantee
- Off-platform contact push in a financial context
- Undisclosed promotion of financial product or crypto asset
- Partial impersonation signals without explicit false claim
- Language suggesting guaranteed outcomes without stating them directly

**Default action:** escalate_review
**Review requirement:** Human review within 24 hours

---

## LOW (Risk Weight: 1) → allow

Assign LOW when content:
- Mentions financial products without violation signals
- Discusses investment topics in general educational terms
- Contains weak or ambiguous signals only
- Is clearly satirical or journalistic in nature

**Default action:** allow
**Review requirement:** None — monitor only

---

## Ambiguity Decision Tree
```
Is content clearly educational or news?
  YES → LOW → allow
  NO  ↓
Does content contain any HIGH signal?
  YES → HIGH → remove
  NO  ↓
Does content contain any MEDIUM signal?
  YES → MEDIUM → escalate_review
  NO  ↓
LOW → allow
```

---

## Edge Case Handling

If content triggers both HIGH and MEDIUM signals:
→ Assign HIGH.

If content triggers multiple violation patterns:
→ Assign the most severe violation code.

If content is unclear but financially related:
→ Default to MEDIUM and escalate_review.

---

## Key Principle
When uncertain between two severity levels:
**Always assign the higher severity.**
Recall is prioritized over precision in this system.
A missed high-severity violation is more costly than a false positive.
