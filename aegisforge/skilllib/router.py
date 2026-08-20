from __future__ import annotations

from dataclasses import dataclass
import re
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


@dataclass(frozen=True)
class RouteExplanation:
    selected: tuple[Match, ...]
    rejected: tuple[Match, ...]
    query: str
    harness: str | None = None


def _tokens(text: str) -> set[str]:
    return {token for token in TOKEN_RE.findall(text.lower()) if token not in STOPWORDS}


def _eligible(record: SkillRecord, harness: str | None) -> bool:
    if harness is None:
        return True
    return harness.lower() in {item.lower() for item in record.compatible_harnesses}


def search(
    records: Iterable[SkillRecord],
    query: str,
    limit: int = 10,
    *,
    harness: str | None = None,
) -> list[Match]:
    """Search skill metadata deterministically and explain every positive match."""
    if limit <= 0:
        return []
    query_tokens = _tokens(query)
    if not query_tokens:
        return []
    exact_query = query.lower().strip()
    matches: list[Match] = []
    for record in records:
        if not _eligible(record, harness):
            continue
        score = 0.0
        reasons: list[str] = []
        searchable = record.searchable_text()
        keywords = {item.lower() for item in record.keywords}
        domains = {item.lower() for item in record.domains}
        if exact_query and exact_query in searchable:
            score += 6.0
            reasons.append("exact phrase appears in metadata")
        for token in sorted(query_tokens):
            if token in keywords:
                score += 4.0
                reasons.append(f"keyword:{token}")
            elif token in domains:
                score += 3.0
                reasons.append(f"domain:{token}")
            elif token in searchable:
                score += 1.0
                reasons.append(f"metadata:{token}")
        if score:
            matches.append(Match(record, score, tuple(reasons)))
    matches.sort(key=lambda item: (-item.score, item.record.id))
    return matches[:limit]


def _rank_score(match: Match) -> float:
    status_bonus = {"stable": 1.5, "experimental": 0.3, "draft": 0.0, "deprecated": -3.0, "archived": -5.0}
    risk_penalty = {"none": 0.2, "low": 0.1, "moderate": 0.0, "high": -0.2, "critical": -0.4}
    return match.score + status_bonus.get(match.record.status, 0.0) + risk_penalty.get(match.record.risk_level, 0.0)


def explain_route(
    records: Iterable[SkillRecord],
    query: str,
    limit: int = 5,
    *,
    harness: str | None = None,
) -> RouteExplanation:
    """Return selected matches plus rejected alternatives and their ranking scores."""
    candidates = search(records, query, limit=max(limit * 4, 20), harness=harness)
    ranked = [Match(item.record, _rank_score(item), item.reasons) for item in candidates]
    ranked.sort(key=lambda item: (-item.score, item.record.id))
    return RouteExplanation(tuple(ranked[:limit]), tuple(ranked[limit:]), query, harness)


def route(
    records: Iterable[SkillRecord],
    query: str,
    limit: int = 5,
    *,
    harness: str | None = None,
) -> list[Match]:
    """Return the smallest likely set, preferring stable skills and lower risk."""
    return list(explain_route(records, query, limit, harness=harness).selected)
