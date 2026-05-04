"""Resounding Crescendo Index scoring."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .schemas import RCIScore, Verdict


SIGNAL_NAMES = (
    "mention_velocity_zscore",
    "unique_author_growth",
    "engagement_weighted_mentions",
    "meme_variant_growth",
    "cross_surface_spread",
    "contract_or_ticker_proximity",
    "holder_growth_signal",
    "liquidity_growth_signal",
    "bot_chaff_penalty",
    "whale_concentration_penalty",
    "wash_volume_penalty",
)

DEFAULT_WEIGHTS: dict[str, float] = {
    "mention_velocity_zscore": 1.2,
    "unique_author_growth": 1.1,
    "engagement_weighted_mentions": 0.8,
    "meme_variant_growth": 0.7,
    "cross_surface_spread": 1.0,
    "contract_or_ticker_proximity": 1.0,
    "holder_growth_signal": 1.2,
    "liquidity_growth_signal": 1.0,
    "bot_chaff_penalty": -1.5,
    "whale_concentration_penalty": -1.2,
    "wash_volume_penalty": -1.3,
}


def clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def _parse_simple_yaml_mapping(text: str, section: str) -> dict[str, float]:
    """Parse the small key/value YAML shape used by this repo.

    This intentionally avoids a PyYAML dependency. It supports:

    section:
      key: 1.0
    """

    values: dict[str, float] = {}
    in_section = False
    for raw_line in text.splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        if not line:
            continue
        if not line.startswith((" ", "\t")):
            key = line.rstrip(":").strip()
            in_section = key == section
            continue
        if not in_section or ":" not in line:
            continue
        key, raw_value = line.strip().split(":", 1)
        raw_value = raw_value.strip().strip('"').strip("'")
        values[key.strip()] = float(raw_value)
    return values


def load_weights(path: str | Path | None = None) -> dict[str, float]:
    """Load RCI weights from JSON or the local simple YAML format."""

    if path is None:
        return dict(DEFAULT_WEIGHTS)
    weight_path = Path(path)
    if not weight_path.exists():
        return dict(DEFAULT_WEIGHTS)
    text = weight_path.read_text(encoding="utf-8")
    if weight_path.suffix.lower() == ".json":
        raw = json.loads(text)
        raw_weights = raw.get("rci_weights", raw)
    else:
        raw_weights = _parse_simple_yaml_mapping(text, "rci_weights")
    weights = dict(DEFAULT_WEIGHTS)
    for key, value in raw_weights.items():
        if key in SIGNAL_NAMES:
            weights[key] = float(value)
    return weights


def rci_band(score: float) -> str:
    if score >= 86:
        return "Boss drop"
    if score >= 71:
        return "Strong crescendo"
    if score >= 51:
        return "Credible joke rebound"
    if score >= 26:
        return "Possible local echo"
    return "Noise floor"


def verdict_for(score: float, signals: dict[str, float]) -> Verdict:
    hard_chaff = (
        signals.get("bot_chaff_penalty", 0.0) >= 0.85
        or signals.get("whale_concentration_penalty", 0.0) >= 0.85
        or signals.get("wash_volume_penalty", 0.0) >= 0.85
    )
    if hard_chaff and score < 71:
        return Verdict.CHAFF
    if score >= 51:
        return Verdict.WHEAT
    if score >= 26:
        return Verdict.UNCLEAR
    return Verdict.CHAFF


def calculate_rci(
    signals: dict[str, Any],
    weights: dict[str, float] | None = None,
    event_id: str = "",
) -> RCIScore:
    """Calculate a transparent 0-100 RCI score from normalized signals.

    Input signals should be normalized to 0..1. Positive signals raise the
    score. Penalty signals reduce it. This first-pass scorer is deliberately
    simple and tunable so receipt readers can inspect the math.
    """

    active_weights = dict(DEFAULT_WEIGHTS if weights is None else weights)
    normalized = {
        name: clamp(float(signals.get(name, 0.0)), 0.0, 1.0)
        for name in SIGNAL_NAMES
    }

    positive: dict[str, float] = {}
    penalties: dict[str, float] = {}
    positive_weight_total = 0.0
    penalty_weight_total = 0.0
    positive_total = 0.0
    penalty_total = 0.0

    for name, value in normalized.items():
        weight = float(active_weights.get(name, DEFAULT_WEIGHTS[name]))
        contribution = value * weight
        if weight >= 0:
            positive[name] = round(contribution, 4)
            positive_weight_total += weight
            positive_total += contribution
        else:
            penalty_value = value * abs(weight)
            penalties[name] = round(penalty_value, 4)
            penalty_weight_total += abs(weight)
            penalty_total += penalty_value

    base_score = 0.0
    if positive_weight_total:
        base_score = (positive_total / positive_weight_total) * 100.0

    penalty_points = 0.0
    if penalty_weight_total:
        penalty_points = (penalty_total / penalty_weight_total) * 40.0

    score = round(clamp(base_score - penalty_points), 2)
    return RCIScore(
        event_id=event_id,
        score=score,
        verdict=verdict_for(score, normalized),
        band=rci_band(score),
        signals=normalized,
        positive_contributions=positive,
        penalty_contributions=penalties,
    )
