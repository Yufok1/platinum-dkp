# Wheat Farm ZEUS Implementation Plan

## Receipt

Agent: ZEUS
Action: prepare local MVP scaffold
Action class: write, operator-approved by direct "make it so" instruction
Target: `platinum-dkp` repo
State changed: yes
Risk level: low; local code, fixtures, docs, and no live external adapters
Rollback path: revert the commit that adds the Wheat Farm scaffold

## Objective

Build Wheat Farm as a guarded, public-signal, value-only correlation engine. The first deliverable is local-only and fixture-backed:

```text
Event -> snapshots -> RCI score -> Wheat / Chaff / Unclear -> public receipt
```

## Implemented Layout

```text
wheatfarm/
  __init__.py
  __main__.py
  access_policy.py
  adapters.py
  cli.py
  rci.py
  receipts.py
  schemas.py
config/
  access_policy.yaml
  rci_weights.yaml
fixtures/
  fixture_event_clean_wheat.json
  fixture_event_fake_pump_mimic.json
  fixture_event_social_only_no_value.json
  fixture_event_value_only_no_social.json
  fixture_event_whale_dominated.json
  fixture_event_bot_chaff.json
tests/
  test_wheatfarm.py
```

## Hard Boundary

This MVP performs no live scraping, trading, wallet targeting, private-data collection, botting, amplification, or market activity. It only reads local fixtures and configuration.

Ray-variable amounts remain lore labels, event IDs, receipt tags, or dashboard motifs. They are not buy instructions.

## CLI Shape

```bash
python -m wheatfarm fixtures list
python -m wheatfarm rci score --fixture fixture_event_clean_wheat
python -m wheatfarm rci score --fixture fixture_event_clean_wheat --json
python -m wheatfarm receipt generate --fixture fixture_event_clean_wheat
python -m wheatfarm policy classify --action write
```

## Scoring Model

The first RCI scorer expects normalized 0..1 signals and reads weights from `config/rci_weights.yaml`.

Positive signals raise the score. Penalty signals reduce it. Heavy bot, whale, or wash flags can force a Chaff verdict unless the score is strong enough to deserve deeper review.

## Fixtures

The six fixtures exercise the first expected Wheat Farm verdicts:

- clean wheat
- fake pump mimic
- social-only/no-value
- value-only/no-social
- whale-dominated
- bot chaff

Each fixture includes event data, normalized signals, snapshots, expected RCI range, and expected verdict.

## Next Build Slice

1. Add JSON schema validation for fixture and receipt files.
2. Add read-only DEX Screener adapter behind an explicit `--live-read` flag.
3. Add read-only CoinGecko/GeckoTerminal adapter behind the same gate.
4. Add a manual event ledger command that prepares a diff but does not write until approval is recorded.
5. Add a static dashboard export from fixture data.
