"""
src/metrics_logger.py
Persists evaluation run metrics to logs/eval_runs/.
Enables prompt version comparison over time.
"""

import jsonlines
from pathlib import Path
from datetime import datetime
import config

LOG_DIR = Path("logs/eval_runs")

def log_run(metrics: dict) -> dict:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "provider": config.LLM_PROVIDER,
        "model": config.LLM_MODEL,
        **metrics
    }
    with jsonlines.open(LOG_DIR / "eval_log.jsonl", "a") as writer:
        writer.write(entry)
    return entry

def load_all_runs() -> list:
    log_path = LOG_DIR / "eval_log.jsonl"
    if not log_path.exists():
        return []
    with jsonlines.open(log_path) as reader:
        return list(reader)
