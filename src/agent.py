"""
src/agent.py
Core classification agent.
Calls LLM, parses structured output, returns AgentOutput.
Parse failure defaults to escalate_review — never silent allow.
"""

import json
import re
from src.llm_client import LLMClient
from src.prompt_builder import PromptBuilder
from src.schema import AgentOutput
import config

PARSE_ERROR_DEFAULT = {
    "label": 1,
    "category": "none",
    "violation": "PARSE_ERROR",
    "severity": "medium",
    "enforcement": "escalate_review",
    "rationale": "Model output parsing failed — escalated for safety."
}

class Agent:
    def __init__(self, prompt_version: str = None):
        self.prompt_version = prompt_version or config.DEFAULT_PROMPT_VERSION
        self.llm = LLMClient()
        self.builder = PromptBuilder(self.prompt_version)

    def classify(self, text: str, policy_context: str = None) -> AgentOutput:
        if policy_context:
            prompt = self.builder.build(text=text, policy_context=policy_context)
        else:
            prompt = self.builder.build(text=text)

        response_text, latency_ms = self.llm.generate(prompt)
        parsed = self._parse(response_text)

        # Sentinel key indicates clean parse failure
        if parsed.get("_parse_error"):
            data = PARSE_ERROR_DEFAULT
        else:
            data = {**PARSE_ERROR_DEFAULT, **parsed}

        return AgentOutput(
            label=data["label"],
            domain="financial_integrity",
            category=data["category"],
            violation=data["violation"],
            severity=data["severity"],
            enforcement=data["enforcement"],
            rationale=data["rationale"],
            prompt_version=self.prompt_version,
            latency_ms=round(latency_ms, 2)
        )

    def _parse(self, response_text: str) -> dict:
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", response_text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group())
                except json.JSONDecodeError:
                    pass
        return {"_parse_error": True}
