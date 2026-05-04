# Hugging Face Agent Port

Use this when Platinum DKP should run outside a Custom GPT.

```text
We are the fire that binds.
```

## Goal

Run the same referee contract as a Hugging Face Space, local model wrapper, or simple Python service.

The authority docs are:

- `PLATINUM_DKP_RULEBOOK.md`
- `STATE_MACHINE.md`
- `MARKET_TALK_POLICY.md`
- `TREASURY_GOVERNANCE.md`
- `MODERATION_POLICY.md`
- `QUEST_CATALOG.md`
- `RAID_LAW_GLOSSARY.md`

## Minimal Runtime Shape

```text
user message
-> load authority docs
-> classify
-> route to state
-> produce answer
-> append receipt
```

## Recommended Files To Load As Context

```text
CUSTOM_GPT_INSTRUCTIONS.md
STATE_MACHINE.md
PLATINUM_DKP_RULEBOOK.md
QUEST_CATALOG.md
TREASURY_GOVERNANCE.md
MARKET_TALK_POLICY.md
MODERATION_POLICY.md
DKP_SCORING_TABLE.md
RAID_LAW_GLOSSARY.md
```

Despite the filename, `CUSTOM_GPT_INSTRUCTIONS.md` is mostly a portable referee prompt. If deploying on Hugging Face, rename it or copy its contents into the system prompt for the local model.

## Brotology Install Order

Prefer GitHub when the runtime can install packages:

```bash
pip install git+https://github.com/Yufok1/Brotology-field-guide.git
```

Fallback:

```bash
pip install brotology-field-guide
```

For a static or no-install Space, upload the relevant Brotology text as local files and load them as context.

## API Surface

Useful endpoints if implemented:

```text
POST /classify
POST /quest
POST /score
POST /proposal
POST /appeal
POST /patch-note
GET /rules
GET /health
```

Every response should include:

```text
classification
state
rule
evidence
next_action
```

## Deployment Boundary

Do not put private keys, seed phrases, API secrets, treasury credentials, or wallet credentials into Hugging Face repository files, Space variables, public logs, or model context.

Use secrets only for service credentials the Space needs, never for wallet custody.
