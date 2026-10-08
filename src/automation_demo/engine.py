from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from enum import Enum
import hashlib
import re
from typing import Iterable


class Decision(str, Enum):
    AUTOMATE = "automate"
    REQUIRE_APPROVAL = "require_approval"
    MANUAL = "manual"
    DUPLICATE = "duplicate"


@dataclass(frozen=True)
class Request:
    request_id: str
    category: str
    summary: str
    requester_email: str


@dataclass(frozen=True)
class EvidenceEvent:
    timestamp: str
    request_id: str
    decision: str
    reason: str
    summary_redacted: str
    evidence_hash: str


SAFE_CATEGORIES = {"invoice_copy", "service_status", "usage_summary"}
SENSITIVE_CATEGORIES = {
    "quota_change",
    "payment_method_update",
    "account_deletion",
    "marketing_opt_out",
}


def redact(text: str) -> str:
    """Remove common contact details before writing evidence or calling an LLM."""
    text = re.sub(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", "[EMAIL]", text)
    return re.sub(r"(?<!\w)(?:\+?\d[\d .()-]{7,}\d)(?!\w)", "[PHONE]", text)


class AutomationEngine:
    """A deterministic policy boundary around an automation action layer."""

    def __init__(self) -> None:
        self._processed: set[str] = set()
        self.evidence: list[EvidenceEvent] = []

    def process(self, request: Request) -> Decision:
        if request.request_id in self._processed:
            return self._record(request, Decision.DUPLICATE, "idempotency key already processed")

        self._processed.add(request.request_id)
        if request.category in SAFE_CATEGORIES:
            return self._record(request, Decision.AUTOMATE, "category is safe for the mock action layer")
        if request.category in SENSITIVE_CATEGORIES:
            return self._record(request, Decision.REQUIRE_APPROVAL, "category can change customer data or access")
        return self._record(request, Decision.MANUAL, "category has no approved automation policy")

    def process_many(self, requests: Iterable[Request]) -> list[Decision]:
        return [self.process(request) for request in requests]

    def _record(self, request: Request, decision: Decision, reason: str) -> Decision:
        clean_summary = redact(request.summary)
        digest_input = f"{request.request_id}|{decision}|{reason}|{clean_summary}"
        event = EvidenceEvent(
            timestamp=datetime.now(timezone.utc).isoformat(),
            request_id=request.request_id,
            decision=decision.value,
            reason=reason,
            summary_redacted=clean_summary,
            evidence_hash=hashlib.sha256(digest_input.encode("utf-8")).hexdigest(),
        )
        self.evidence.append(event)
        return decision

    def evidence_as_dicts(self) -> list[dict[str, str]]:
        return [asdict(event) for event in self.evidence]

