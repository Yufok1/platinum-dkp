"""Public receipt rendering for Wheat Farm."""

from __future__ import annotations

from typing import Any

from .schemas import Event, RCIScore


def _value(snapshot: dict[str, Any], key: str) -> str:
    value = snapshot.get(key)
    if value is None:
        return "unknown"
    return str(value)


def render_public_receipt(fixture: dict[str, Any], score: RCIScore) -> str:
    event = Event.from_mapping(fixture["event"])
    snapshots = fixture.get("snapshots", {})
    baseline = snapshots.get("t_minus_24h", {})
    plus_24h = snapshots.get("t_plus_24h", {})
    plus_72h = snapshots.get("t_plus_72h", {})

    lines = [
        "WHEAT FARM RECEIPT",
        "",
        f"Event: {event.name}",
        f"Timestamp UTC: {event.timestamp_utc}",
        f"Token: {event.token_ticker}",
        f"Contract: {event.contract_address}",
        f"Chain: {event.chain}",
        "",
        "T-24h Baseline:",
        f"- Price: {_value(baseline, 'price')}",
        f"- Liquidity: {_value(baseline, 'liquidity')}",
        f"- Holders: {_value(baseline, 'holders')}",
        f"- Mentions/hour: {_value(baseline, 'mentions_per_hour')}",
        "",
        "T+24h:",
        f"- Price change: {_value(plus_24h, 'price_change_percent')}",
        f"- Liquidity change: {_value(plus_24h, 'liquidity_change_percent')}",
        f"- New holders: {_value(plus_24h, 'new_holders')}",
        f"- Unique authors: {_value(plus_24h, 'unique_authors')}",
        f"- RCI: {score.score} ({score.band})",
        "",
        "T+72h:",
        f"- Retained holders: {_value(plus_72h, 'retained_holders')}",
        f"- Top-holder concentration: {_value(plus_72h, 'top_10_holder_percent')}",
        f"- Verdict: {score.verdict.value}",
        "",
        "Correlation Claim:",
        "This is a public-signal, value-only correlation receipt. It does not prove causation, provide financial advice, or instruct anyone to buy, sell, hold, or coordinate activity.",
    ]
    return "\n".join(lines)
