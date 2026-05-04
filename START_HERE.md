# Start Here

This is the 90-second door.

## What This Is

Platinum DKP is a joke-and-receipt game around a meme coin community.

The token is the banner. DKP is the off-chain honor ledger. Quests are community contributions. Receipts are the loot log.

Wheat Farm is the analytics layer. It checks whether a joke, meme, song, post, or public bit creates a measurable public rebound.

## Why It Matters

Most meme-coin stories stop at vibes or price screenshots. Wheat Farm asks for better evidence:

- did more unique public people repeat the joke?
- did the joke spread across surfaces?
- did value-only metrics move near the event?
- did new holders stay after the first spike?
- did holder distribution stay healthy enough to avoid a fake-pump read?

The output is simple:

```text
Wheat / Chaff / Unclear
```

## What It Does Not Claim

This is not financial advice.

It does not tell anyone to buy, sell, hold, or coordinate.

It does not prove price causation by default.

It does not scrape private data, target wallets, use secrets, or manufacture engagement.

Ray-variable amounts are lore labels, receipt IDs, or dashboard motifs. They are not buy instructions.

## Try The Local Demo

Run from the repo root:

```bash
python -m wheatfarm fixtures list
```

Score the clean Wheat fixture:

```bash
python -m wheatfarm rci score --fixture fixture_event_clean_wheat
```

Generate a public receipt:

```bash
python -m wheatfarm receipt generate --fixture fixture_event_clean_wheat
```

Run quality control:

```bash
python -m unittest discover -s tests
```

The demo is fixture-backed only. It does not call live APIs.

## What To Upload To A GPT

Use these first:

- `START_HERE.md`
- `CUSTOM_GPT_INSTRUCTIONS.md`
- `STATE_MACHINE.md`
- `PLATINUM_DKP_RULEBOOK.md`
- `MARKET_TALK_POLICY.md`
- `RAID_LAW_GLOSSARY.md`
- `WHEAT_FARM_RECEIPT_TEMPLATE.md`
- `docs/WHEAT_FARM_ZEUS_IMPLEMENTATION_PLAN.md`

Optional Brotology support:

- `WHEAT_FARM_CONTINUITY_IDEATION_REPORT_2026-05-04.md`
- `RAY_VARIABLE_REGISTRY_AND_PI_BAG_AUDIO_EMOTES_2026-05-04.md`
- `CHAMPION_COUNCIL_BROTOLOGY_CONTINUITY_LINK_FIELD_REPORT_2026-05-04.md`

## First User Test Prompt

```text
Using Wheat Farm, help me create the first public receipt. Ask me only for the minimum public data needed. Classify unknowns clearly and do not give trading advice.
```

## Quality Bar

A stranger should understand this in under 90 seconds:

- Platinum DKP is the game layer.
- Wheat Farm is the proof layer.
- RCI is the evidence score.
- Verdicts are Wheat, Chaff, or Unclear.
- Receipts matter more than vibes.
