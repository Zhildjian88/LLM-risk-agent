"""
src/schema.py
Shared output schema for all agent predictions.
Every classification returns this structure — consistent across
all prompt versions and evaluation runs.
"""

from dataclasses import dataclass, asdict
import json

@dataclass
class AgentOutput:
    label: int              # 0 = benign, 1 = violation
    domain: str             # "financial_integrity"
    category: str           # e.g. "investment_scam"
    violation: str          # e.g. "GUARANTEED_RETURN"
    severity: str           # "low" | "medium" | "high"
    enforcement: str        # "allow" | "escalate_review" | "remove"
    rationale: str          # concise explanation
    prompt_version: str     # e.g. "v2_hierarchical"
    latency_ms: float       # measured per call

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)
