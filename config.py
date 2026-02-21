"""
config.py
Single source of truth for all project settings.
Provider and model controlled via environment — not hardcoded.
"""
import os

# LLM Provider — set via environment variable
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "anthropic")
LLM_MODEL = os.getenv("LLM_MODEL", "claude-haiku-4-5-20251001")

# Paths
POLICY_PATH = "policy/policy.md"
REASON_CODES_PATH = "policy/reason_codes.json"
GOLD_DATA_PATH = "data/gold_cases.jsonl"
DRIFT_DATA_PATH = "data/drift_cases.jsonl"
PROMPT_DIR = "prompts/"
DEFAULT_PROMPT_VERSION = "v1_baseline"

# Evaluation thresholds
HIGH_SEVERITY_RECALL_THRESHOLD = 0.85
LATENCY_P95_THRESHOLD_MS = 6000
