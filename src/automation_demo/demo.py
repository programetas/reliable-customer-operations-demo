from __future__ import annotations

import json
from pathlib import Path

from .engine import AutomationEngine, Request


def main() -> None:
    source = Path(__file__).parents[2] / "sample_data" / "requests.json"
    requests = [Request(**item) for item in json.loads(source.read_text(encoding="utf-8"))]
    engine = AutomationEngine()

    for request, decision in zip(requests, engine.process_many(requests), strict=True):
        print(f"{request.request_id}: {decision.value}")

    print(json.dumps(engine.evidence_as_dicts(), indent=2))


if __name__ == "__main__":
    main()

