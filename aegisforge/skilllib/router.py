"""Explainable, dependency-free skill search and routing."""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

from .registry import SkillRecord

TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9+#.-]*")
STOPWORDS = {
    "a", "an", "and", "are", "be", "by", "for", "from", "how", "i", "in",
    "into", "is", "it", "me", "my", "of", "on", "or", "the", "this", "to", "with",
}


@dataclass(frozen=True)
class Match:
    record: SkillRecord
    score: float
    reasons: tuple[str, ...]


def _tokens(text: str) -> set[str]:
    return {token for token in TOKEN_RE.findall(text.lower()) if token not in STOPWORDS}


def search(records: Iterable[SkillRecord], query: str, limit: int = 10) -> list[Match]:
    query_tokens = _tokens(query)
    if not query_tokens:
        return []
    matches: list[Match] = []
    for record in records:
        score = 0.0
        reasons: list[str] = []
        exact_query = query.lower().strip()
        if exact_query and exact_query in record.searchable_text():
            score += 6.0
            reasons.append("exact phrase appears in metadata")
        for token in sorted(query_tokens):
            if token in {item.lower() for item in record.keywords}:
                score += 4.0
                reasons.append(f"keyword:{token}")
            elif token in {item.lower() for item in record.domains}:
                score += 3.0
                reasons.append(f"domain:{token}")
            elif token in record.searchable_text():
                score += 1.0
                reasons.append(f"metadata:{token}")
        if score:
            matches.append(Match(record, score, tuple(reasons)))
    matches.sort(key=lambda item: (-item.score, item.record.id))
    return matches[:limit]


def route(records: Iterable[SkillRecord], query: str, limit: int = 5) -> list[Match]:
    """Return the smallest likely set, preferring stable skills and lower risk."""
    matches = search(records, query, limit=max(limit * 3, 10))
    status_bonus = {"stable": 1.5, "verified": 1.2, "experimental": 0.3, "draft": 0.0, "deprecated": -3.0, "archived": -5.0}
    risk_penalty = {"none": 0.2, "low": 0.1, "moderate": 0.0, "high": -0.2, "critical": -0.4}
    ranked = [
        Match(
            item.record,
            item.score + status_bonus.get(item.record.status, 0) + risk_penalty.get(item.record.risk_level, 0),
            item.reasons,
        )
        for item in matches
    ]
    ranked.sort(key=lambda item: (-item.score, item.record.id))
    return ranked[:limit]
