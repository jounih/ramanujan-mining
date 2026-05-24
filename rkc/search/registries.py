"""rkc.search.registries — JsonlRegistry: accepted-identities log + reject log.

The "store accepted or reject with reason" step 6 of Project C. Per
PROJECT_C_DESIGN.md "Critical engineering decisions" §3: the reject-with-
failure-reason log is methodologically critical (the analogue of
DID_NOT_PAN_OUT for the automated search).

The JsonlRegistry writes two JSONL files:
  - accepted.jsonl: one record per accepted SearchOutcome
  - rejected.jsonl: one record per rejected SearchOutcome (with named reason)
"""
from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import sympy as sp

from .core import RejectReason, Registry, SearchOutcome


@dataclass
class JsonlRegistry:
    """Append-only JSONL registry of accepted identities + reject log.

    Idempotency: `is_known` checks the SHA-256 of the (before, after)
    pair as the dedup key. The same transformation can be re-proposed
    many times by the random proposer; only the first acceptance is
    stored.
    """
    accepted_path: Path
    rejected_path: Path
    _seen_hashes: set[str] | None = None

    @classmethod
    def with_dir(cls, dir_path: str | Path) -> "JsonlRegistry":
        """Convenience: create the directory if needed and place
        accepted.jsonl + rejected.jsonl inside."""
        d = Path(dir_path)
        d.mkdir(parents=True, exist_ok=True)
        return cls(accepted_path=d / "accepted.jsonl",
                   rejected_path=d / "rejected.jsonl")

    def _hash_outcome(self, outcome: SearchOutcome) -> str:
        """Content-addressable hash of (state_before, state_after)."""
        h = hashlib.sha256()
        h.update(str(outcome.state_before.payload).encode("utf-8"))
        h.update(b"||")
        h.update(str(outcome.state_after.payload).encode("utf-8"))
        return h.hexdigest()[:16]  # 16 chars is plenty for dedup

    def _load_seen(self) -> set[str]:
        """Lazy-load seen hashes from accepted.jsonl on first call."""
        if self._seen_hashes is not None:
            return self._seen_hashes
        self._seen_hashes = set()
        if self.accepted_path.exists():
            with self.accepted_path.open() as f:
                for line in f:
                    try:
                        rec = json.loads(line)
                        if "hash" in rec:
                            self._seen_hashes.add(rec["hash"])
                    except json.JSONDecodeError:
                        continue
        return self._seen_hashes

    def is_known(self, outcome: SearchOutcome) -> bool:
        return self._hash_outcome(outcome) in self._load_seen()

    def store(self, outcome: SearchOutcome) -> str:
        h = self._hash_outcome(outcome)
        self._load_seen().add(h)
        rec = {
            "hash": h,
            "timestamp": time.time(),
            "state_before": str(outcome.state_before.payload),
            "state_before_meta": _str_keys(outcome.state_before.metadata),
            # v0.9a: persist top-level convergence_class explicitly on both
            # sides (in addition to its appearance in *_meta via the
            # _str_keys dump of metadata). Direct field access at audit
            # time saves a string-parse of the meta dict.
            "state_before_convergence_class": outcome.state_before.convergence_class,
            "op_sequence": [
                {"op_id": op.op_id, "params": _str_keys(op.params), "confidence": op.confidence}
                for op in outcome.op_sequence
            ],
            "state_after": str(outcome.state_after.payload),
            "state_after_meta": _str_keys(outcome.state_after.metadata),
            "state_after_convergence_class": outcome.state_after.convergence_class,
            "verification_digits": outcome.verification.digits_or_examples,
            "verification_reason": outcome.verification.reason,
            "cost_direct": outcome.cost.direct_cost,
            "cost_reduced": outcome.cost.reduced_cost,
            "cost_ratio": outcome.cost.improvement_ratio,
            "cost_notes": outcome.cost.notes,
            "route": outcome.route,
            "notes": outcome.notes,
        }
        self.accepted_path.parent.mkdir(parents=True, exist_ok=True)
        with self.accepted_path.open("a") as f:
            f.write(json.dumps(rec, default=str) + "\n")
        return h

    def reject(self, outcome: SearchOutcome, reason: RejectReason) -> None:
        rec = {
            "timestamp": time.time(),
            "state_before": str(outcome.state_before.payload),
            "op_sequence": [
                {"op_id": op.op_id, "confidence": op.confidence}
                for op in outcome.op_sequence
            ],
            "state_after": str(outcome.state_after.payload),
            "reject_reason": reason.value,
            "verification_reason": outcome.verification.reason if outcome.verification else None,
            "cost_notes": outcome.cost.notes if outcome.cost else None,
            "route": outcome.route,
        }
        self.rejected_path.parent.mkdir(parents=True, exist_ok=True)
        with self.rejected_path.open("a") as f:
            f.write(json.dumps(rec, default=str) + "\n")


def _str_keys(d: dict[Any, Any]) -> dict[str, str]:
    """JSONL-safe stringification of dict keys + non-serializable values."""
    return {str(k): str(v) for k, v in d.items()}


# Protocol sanity check
assert isinstance(JsonlRegistry(Path("/tmp/a.jsonl"), Path("/tmp/r.jsonl")), Registry)
