"""Read-only adapter interfaces and local fixture store."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .rci import calculate_rci, load_weights
from .schemas import Event, RCIScore


class ReadOnlyAdapterError(RuntimeError):
    """Raised when a read-only adapter cannot satisfy a request."""


class FixtureStore:
    """Repo-backed read-only fixture adapter."""

    def __init__(self, fixture_dir: str | Path) -> None:
        self.fixture_dir = Path(fixture_dir)

    def list_fixture_ids(self) -> list[str]:
        if not self.fixture_dir.exists():
            return []
        return sorted(path.stem for path in self.fixture_dir.glob("fixture_*.json"))

    def load_fixture(self, fixture_id: str) -> dict[str, Any]:
        safe_id = fixture_id.removesuffix(".json")
        path = self.fixture_dir / f"{safe_id}.json"
        if not path.exists():
            raise ReadOnlyAdapterError(f"fixture not found: {safe_id}")
        return json.loads(path.read_text(encoding="utf-8"))

    def load_event(self, fixture_id: str) -> Event:
        fixture = self.load_fixture(fixture_id)
        return Event.from_mapping(fixture["event"])

    def score_fixture(
        self,
        fixture_id: str,
        weights_path: str | Path | None = None,
    ) -> RCIScore:
        fixture = self.load_fixture(fixture_id)
        event = Event.from_mapping(fixture["event"])
        return calculate_rci(
            fixture.get("signals", {}),
            weights=load_weights(weights_path),
            event_id=event.event_id,
        )


class PublicSignalAdapter:
    """Interface placeholder for future public-only adapters."""

    def get_token_value_snapshot(self, token: str, timestamp_window: str) -> dict[str, Any]:
        raise NotImplementedError("read-only adapter stub")

    def get_holder_snapshot(self, token: str, timestamp_window: str) -> dict[str, Any]:
        raise NotImplementedError("read-only adapter stub")

    def search_public_mentions(self, query: str, timestamp_window: str) -> list[dict[str, Any]]:
        raise NotImplementedError("read-only adapter stub")

    def get_media_artifact_metrics(self, artifact: str, timestamp_window: str) -> dict[str, Any]:
        raise NotImplementedError("read-only adapter stub")
