"""Approval gate policy for Wheat Farm actions."""

from __future__ import annotations

from pathlib import Path


DEFAULT_POLICY: dict[str, list[str]] = {
    "safe_auto_approve": [
        "read",
        "get",
        "list",
        "search",
        "status",
        "info",
        "tree",
        "catalog",
        "inspect",
        "diff_preview",
    ],
    "manual_approval_required": [
        "write",
        "edit",
        "append",
        "update",
        "mutate",
        "delete",
        "rename",
        "copy",
        "restore",
        "execute",
        "run",
        "deploy",
        "train",
        "plug",
        "proxy",
        "regenerate",
        "verify_execute",
    ],
    "absolute_safety_gates": [
        "private keys",
        "seed phrases",
        "wallet credentials",
        "api secrets",
        "session cookies",
        "private account data",
        "non-public personal information",
    ],
}


def _parse_simple_yaml_lists(text: str) -> dict[str, list[str]]:
    policy: dict[str, list[str]] = {}
    current: str | None = None
    for raw_line in text.splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        if not line:
            continue
        if not line.startswith((" ", "\t", "-")):
            current = line.rstrip(":").strip()
            policy.setdefault(current, [])
            continue
        if current and line.strip().startswith("- "):
            policy[current].append(line.strip()[2:].strip().strip('"').strip("'"))
    return policy


def load_access_policy(path: str | Path | None = None) -> dict[str, list[str]]:
    if path is None:
        return {key: list(value) for key, value in DEFAULT_POLICY.items()}
    policy_path = Path(path)
    if not policy_path.exists():
        return {key: list(value) for key, value in DEFAULT_POLICY.items()}
    loaded = _parse_simple_yaml_lists(policy_path.read_text(encoding="utf-8"))
    merged = {key: list(value) for key, value in DEFAULT_POLICY.items()}
    for key, value in loaded.items():
        if key in merged:
            merged[key] = value
    return merged


def classify_action(action: str, policy: dict[str, list[str]] | None = None) -> str:
    active_policy = DEFAULT_POLICY if policy is None else policy
    normalized = action.strip().lower().replace("-", "_")
    if normalized in active_policy.get("safe_auto_approve", []):
        return "safe_read_only"
    if normalized in active_policy.get("manual_approval_required", []):
        return "manual_approval_required"
    return "unknown_requires_review"
