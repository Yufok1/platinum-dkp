"""Command-line interface for the Wheat Farm local MVP."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .access_policy import classify_action, load_access_policy
from .adapters import FixtureStore
from .rci import load_weights
from .receipts import render_public_receipt


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FIXTURES = REPO_ROOT / "fixtures"
DEFAULT_WEIGHTS = REPO_ROOT / "config" / "rci_weights.yaml"
DEFAULT_POLICY = REPO_ROOT / "config" / "access_policy.yaml"


def _fixture_store(args: argparse.Namespace) -> FixtureStore:
    return FixtureStore(Path(args.fixture_dir))


def cmd_fixtures_list(args: argparse.Namespace) -> int:
    store = _fixture_store(args)
    for fixture_id in store.list_fixture_ids():
        print(fixture_id)
    return 0


def cmd_rci_score(args: argparse.Namespace) -> int:
    store = _fixture_store(args)
    score = store.score_fixture(args.fixture, args.weights)
    if args.json:
        print(
            json.dumps(
                {
                    "event_id": score.event_id,
                    "score": score.score,
                    "band": score.band,
                    "verdict": score.verdict.value,
                    "signals": score.signals,
                    "positive_contributions": score.positive_contributions,
                    "penalty_contributions": score.penalty_contributions,
                },
                indent=2,
                sort_keys=True,
            )
        )
    else:
        print(f"{score.event_id}: RCI {score.score} - {score.band} - {score.verdict.value}")
    return 0


def cmd_receipt_generate(args: argparse.Namespace) -> int:
    store = _fixture_store(args)
    fixture = store.load_fixture(args.fixture)
    score = store.score_fixture(args.fixture, args.weights)
    print(render_public_receipt(fixture, score))
    return 0


def cmd_policy_classify(args: argparse.Namespace) -> int:
    policy = load_access_policy(args.policy)
    result = classify_action(args.action, policy)
    payload: dict[str, Any] = {
        "action": args.action,
        "classification": result,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="wheatfarm",
        description="Public-signal, value-only joke rebound analytics.",
    )
    parser.add_argument("--fixture-dir", default=str(DEFAULT_FIXTURES))
    parser.add_argument("--weights", default=str(DEFAULT_WEIGHTS))

    subparsers = parser.add_subparsers(dest="command", required=True)

    fixtures = subparsers.add_parser("fixtures")
    fixtures_sub = fixtures.add_subparsers(dest="fixtures_command", required=True)
    fixtures_list = fixtures_sub.add_parser("list")
    fixtures_list.set_defaults(func=cmd_fixtures_list)

    rci = subparsers.add_parser("rci")
    rci_sub = rci.add_subparsers(dest="rci_command", required=True)
    rci_score = rci_sub.add_parser("score")
    rci_score.add_argument("--fixture", required=True)
    rci_score.add_argument("--json", action="store_true")
    rci_score.set_defaults(func=cmd_rci_score)

    receipt = subparsers.add_parser("receipt")
    receipt_sub = receipt.add_subparsers(dest="receipt_command", required=True)
    receipt_generate = receipt_sub.add_parser("generate")
    receipt_generate.add_argument("--fixture", required=True)
    receipt_generate.set_defaults(func=cmd_receipt_generate)

    policy = subparsers.add_parser("policy")
    policy.add_argument("--policy", default=str(DEFAULT_POLICY))
    policy_sub = policy.add_subparsers(dest="policy_command", required=True)
    policy_classify = policy_sub.add_parser("classify")
    policy_classify.add_argument("--action", required=True)
    policy_classify.set_defaults(func=cmd_policy_classify)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))
