from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path

from .engine import AutomationEngine, Request


CATEGORY_PLAN = (
    ("invoice_copy", 30),
    ("service_status", 20),
    ("quota_change", 15),
    ("payment_method_update", 10),
    ("account_deletion", 5),
    ("custom_contract_question", 10),
    ("technical_investigation", 10),
)


def generate_requests(count: int) -> list[Request]:
    if count < 1:
        raise ValueError("count must be positive")

    weighted_categories = [category for category, weight in CATEGORY_PLAN for _ in range(weight)]
    return [
        Request(
            request_id=f"SIM-{index + 1:04d}",
            category=weighted_categories[index % len(weighted_categories)],
            summary=f"Synthetic request {index + 1} from user{index + 1}@example.test",
            requester_email=f"user{index + 1}@example.test",
        )
        for index in range(count)
    ]


def run_simulation(count: int) -> dict[str, object]:
    engine = AutomationEngine()
    decisions = engine.process_many(generate_requests(count))
    counts = Counter(decision.value for decision in decisions)
    return {
        "scenario": "synthetic_customer_operations",
        "request_count": count,
        "decisions": dict(sorted(counts.items())),
        "redacted_evidence_count": len(engine.evidence),
        "disclaimer": "Synthetic demonstration; not customer performance data.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the synthetic automation simulation")
    parser.add_argument("--count", type=int, default=100)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    report = run_simulation(args.count)
    rendered = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()

