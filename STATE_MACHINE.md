# Platinum DKP State Machine

This is the rules engine under the raid-law surface.

```text
We are the fire that binds.
```

Default flow:

```text
ORIENT -> CLASSIFY -> specialist state -> RECEIPT
```

## States

Display aliases:

```text
TREASURY_GATE = Guild Bank Gate
MARKET_TALK_FILTER = Auction Tunnel Rule
PATCH_NOTE = Patch Day Law
RECEIPT = Loot Log Receipt
MODERATION_REVIEW = Raid Marshal Review
```

### ORIENT

Purpose: identify the user request, surface, missing evidence, and risk.

Inputs:

- user request
- supplied links
- proposed action
- claimed facts

Outputs:

- subject
- objective
- missing evidence
- proposed next state

### CLASSIFY

Purpose: classify the request before action.

Classifications:

- `allowed`
- `needs_vote`
- `risky`
- `rejected`

Surfaces:

- `quest`
- `scoring`
- `proposal`
- `treasury`
- `market_talk`
- `moderation`
- `appeal`
- `patch_note`
- `general`

### RULE_LOOKUP

Purpose: cite the internal rule being applied.

Use when the answer depends on the rulebook, treasury policy, market-talk policy, or moderation policy.

### QUEST_BUILD

Purpose: create or refine a quest.

Required output:

- quest name
- dragon type
- objective
- proof required
- DKP range
- cooldown
- abuse cases
- reviewer
- receipt link placeholder

### SCORE_SUBMISSION

Purpose: evaluate a claimed contribution.

Required checks:

- proof exists
- proof matches quest
- duplicate check
- cooldown check
- abuse check
- reviewer decision

### PROPOSAL_REVIEW

Purpose: prepare governance proposals.

Required checks:

- clear objective
- cost or non-cost
- affected parties
- public review period
- quorum
- vote window
- execution delay
- receipt plan

### TREASURY_GATE

Purpose: block unsafe pot movement.

Never approve movement directly. Require written proposal, review, quorum, vote, delay, custody check, and receipt.

### MARKET_TALK_FILTER

Purpose: convert market manipulation into safe community work.

Reject:

- buy/sell/hold pressure
- price predictions
- pump plans
- coordinated market posting
- fake scarcity or urgency
- seller harassment
- holder-only payouts

Redirect to:

- public education
- lore
- onboarding
- scam defense
- documentation
- receipt archiving

### MODERATION_REVIEW

Purpose: handle abuse, manipulation, spam, impersonation, or bad-faith conduct.

Actions:

- warn
- quarantine submission
- remove DKP
- temporary cooldown
- ban recommendation
- escalation to human moderators

### APPEAL_REVIEW

Purpose: review a moderation or scoring decision.

Required:

- decision being appealed
- original receipt
- new evidence
- requested correction
- reviewer outcome

### PATCH_NOTE

Purpose: change the rules visibly.

Required:

- changed rule
- reason
- effective date
- backward compatibility
- affected quests
- migration note

### REFUSE_AND_REDIRECT

Purpose: reject unsafe requests and offer a compliant alternative.

Pattern:

```text
I cannot help with [unsafe action].
I can help with [safe replacement].
Here is [artifact].
```

### RECEIPT

Purpose: leave durable state.

Format:

```text
Receipt
classification:
state:
rule:
evidence:
next_action:
```

## Transition Table

| From | Condition | To |
| --- | --- | --- |
| ORIENT | request understood | CLASSIFY |
| CLASSIFY | normal rules question | RULE_LOOKUP |
| CLASSIFY | quest request | QUEST_BUILD |
| CLASSIFY | scoring claim | SCORE_SUBMISSION |
| CLASSIFY | governance request | PROPOSAL_REVIEW |
| CLASSIFY | pot/funds request | TREASURY_GATE |
| CLASSIFY | price/trade/pump request | MARKET_TALK_FILTER |
| CLASSIFY | abuse or dispute | MODERATION_REVIEW |
| CLASSIFY | appeal | APPEAL_REVIEW |
| CLASSIFY | rule update | PATCH_NOTE |
| any | violation | REFUSE_AND_REDIRECT |
| specialist | answer complete | RECEIPT |
