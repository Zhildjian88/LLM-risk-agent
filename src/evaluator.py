"""
src/evaluator.py
Runs batch evaluation of agent across a dataset.
Returns per-case results and aggregate metrics.
"""

import jsonlines
import pandas as pd
import time
from src.agent import Agent

class Evaluator:
    def __init__(self, prompt_version: str, dataset_name: str = None, delay_s: float = 0.2):
        self.agent = Agent(prompt_version=prompt_version)
        self.version = prompt_version
        self.dataset_name = dataset_name
        self.delay_s = delay_s

    def run(self, data_path: str) -> pd.DataFrame:
        results = []
        with jsonlines.open(data_path) as reader:
            for case in reader:
                output = self.agent.classify(case["text"])
                results.append({
                    "id": case["id"],
                    "text": case["text"],
                    "true_label": case["label"],
                    "true_severity": case["severity"],
                    "pred_label": output.label,
                    "pred_category": output.category,
                    "pred_violation": output.violation,
                    "pred_severity": output.severity,
                    "pred_enforcement": output.enforcement,
                    "rationale": output.rationale,
                    "prompt_version": self.version,
                    "latency_ms": output.latency_ms,
                    "correct": int(output.label == case["label"]),
                    "is_fn": int(case["label"] == 1 and output.label == 0),
                    "is_fp": int(case["label"] == 0 and output.label == 1),
                })
                time.sleep(self.delay_s)
        return pd.DataFrame(results)

    def metrics(self, df: pd.DataFrame) -> dict:
        tp = len(df[(df.true_label==1) & (df.pred_label==1)])
        fp = len(df[(df.true_label==0) & (df.pred_label==1)])
        fn = len(df[(df.true_label==1) & (df.pred_label==0)])
        tn = len(df[(df.true_label==0) & (df.pred_label==0)])

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall    = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1        = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

        high_df = df[df.true_severity == "high"]
        high_recall = (
            len(high_df[high_df.pred_label==1]) / len(high_df)
            if len(high_df) > 0 else 0
        )

        high_severity_fn_count = int(
            len(df[
                (df.true_severity == "high") &
                (df.true_label == 1) &
                (df.pred_label == 0)
            ])
        )

        parse_error_count = int(
            len(df[df.pred_violation == "PARSE_ERROR"])
        )

        return {
            "prompt_version": self.version,
            "dataset": self.dataset_name,
            "dataset_size": len(df),
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1": round(f1, 4),
            "high_severity_recall": round(high_recall, 4),
            "high_severity_fn_count": high_severity_fn_count,
            "parse_error_count": parse_error_count,
            "tp": tp, "fp": fp, "fn": fn, "tn": tn,
            "p50_latency_ms": round(df.latency_ms.quantile(0.50), 1),
            "p95_latency_ms": round(df.latency_ms.quantile(0.95), 1),
        }
