"""Data shapes for the Wheat Farm local MVP."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Verdict(str, Enum):
    """Public Wheat Farm verdicts."""

    WHEAT = "Wheat"
    CHAFF = "Chaff"
    UNCLEAR = "Unclear"


@dataclass(frozen=True)
class Event:
    """Canonical joke/media event record."""

    event_id: str
    name: str
    timestamp_utc: str
    origin_surface: str
    joke_phrase: str
    token_ticker: str
    contract_address: str
    chain: str
    media_artifact_links: tuple[str, ...] = ()
    meme_variants: tuple[str, ...] = ()
    confidence: str = "operator_supplied"

    @classmethod
    def from_mapping(cls, data: dict[str, Any]) -> "Event":
        return cls(
            event_id=str(data["event_id"]),
            name=str(data["name"]),
            timestamp_utc=str(data["timestamp_utc"]),
            origin_surface=str(data.get("origin_surface", "")),
            joke_phrase=str(data.get("joke_phrase", "")),
            token_ticker=str(data.get("token_ticker", "")),
            contract_address=str(data.get("contract_address", "")),
            chain=str(data.get("chain", "")),
            media_artifact_links=tuple(str(v) for v in data.get("media_artifact_links", ())),
            meme_variants=tuple(str(v) for v in data.get("meme_variants", ())),
            confidence=str(data.get("confidence", "operator_supplied")),
        )


@dataclass(frozen=True)
class Token:
    """Token identity used for value-only correlation."""

    ticker: str
    contract_address: str
    chain: str
    pair_url: str = ""


@dataclass(frozen=True)
class MediaArtifact:
    """Public media object related to a joke event."""

    title: str
    platform: str
    url: str
    hook_phrase: str = ""


@dataclass(frozen=True)
class SocialMention:
    """Aggregated public social mention record."""

    timestamp_utc: str
    surface: str
    phrase: str
    unique_authors: int = 0
    engagement: float = 0.0


@dataclass(frozen=True)
class ValueSnapshot:
    """Value-only token snapshot."""

    window: str
    price: float | None = None
    liquidity: float | None = None
    volume: float | None = None
    buys: int | None = None
    sells: int | None = None
    transactions: int | None = None


@dataclass(frozen=True)
class HolderSnapshot:
    """Public holder distribution snapshot."""

    window: str
    total_holders: int | None = None
    retained_holders: int | None = None
    top_10_holder_percent: float | None = None
    dust_wallet_percent: float | None = None


@dataclass(frozen=True)
class RCIScore:
    """Calculated Resounding Crescendo Index score."""

    event_id: str
    score: float
    verdict: Verdict
    band: str
    signals: dict[str, float] = field(default_factory=dict)
    positive_contributions: dict[str, float] = field(default_factory=dict)
    penalty_contributions: dict[str, float] = field(default_factory=dict)


@dataclass(frozen=True)
class Receipt:
    """Rendered or structured receipt metadata."""

    event_id: str
    verdict: Verdict
    text: str
