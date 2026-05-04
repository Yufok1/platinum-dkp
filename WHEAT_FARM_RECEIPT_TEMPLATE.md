# Wheat Farm Receipt Template

Wheat Farm is the public-signal analytics layer for Platinum DKP. It measures whether a joke, post, song, meme, or raid bit creates a measurable social crescendo that correlates with value-only token movement.

This file is a template, not a trading instruction.

## Hard Boundary

- Public data only.
- No doxxing.
- No private account scraping.
- No coordinated harassment.
- No fake engagement.
- No wash trading.
- No guaranteed price claims.
- No "buy this amount" instructions.
- Ray-variable amounts are lore labels or receipt IDs only.

## First Receipt Form

```text
WHEAT FARM RECEIPT

Event ID:
Event Name:
Timestamp UTC:
Origin Surface:
Joke Phrase:
Meme Variants:
Media Artifact Links:

Token:
Contract:
Chain:
Pair / Pool Link:

T-24h Baseline:
- Price:
- Liquidity:
- Volume:
- Holders:
- Top 10 holder %:
- Mentions/hour:
- Unique authors:

T+15m Ignition:
- Mentions/hour:
- Unique authors:
- Engagement:
- Price change:
- Volume change:

T+1h First Echo:
- Mentions/hour:
- Unique authors:
- Meme variants:
- Price change:
- Liquidity change:

T+24h Holder Check:
- New holders:
- Retained new holders:
- Liquidity change:
- Buy/sell ratio:
- Top 10 holder %:

T+72h Rebound Check:
- Holder retention:
- Price vs baseline:
- Liquidity vs baseline:
- RCI score:
- Verdict: Wheat / Chaff / Unclear

T+7d Conviction Check:
- Retained holders:
- Holder concentration change:
- Social decay or rebound:
- Final verdict:

Operator Notes:
Evidence Links:
Receipt Author:
```

## Resounding Crescendo Index

```text
RCI =
  mention_velocity_zscore
+ unique_author_growth
+ engagement_weighted_mentions
+ meme_variant_growth
+ cross_surface_spread
+ contract_or_ticker_proximity
+ holder_growth_signal
+ liquidity_growth_signal
- bot_chaff_penalty
- whale_concentration_penalty
- wash_volume_penalty
```

Suggested interpretation:

- 0-25: noise floor
- 26-50: possible local echo
- 51-70: credible joke rebound
- 71-85: strong crescendo
- 86-100: boss drop; major public resonance

## Verdicts

Wheat:

The joke produced a measurable crescendo before or alongside the token value move. Mentions, unique authors, holders, and liquidity rose together. Retention survived the 72-hour check. Whale concentration did not worsen.

Chaff:

The token moved, but social signal was weak, copied, late, or bot-heavy. Holder growth did not confirm, or liquidity vanished quickly. The move is likely not a durable joke rebound.

Unclear:

The signal exists but is incomplete. More holder snapshots, social data, or event timing precision is needed before calling it wheat.

## Data Sources To Verify Live

- DEX Screener token-pair endpoints for public pair, liquidity, transaction, volume, and price-change data.
- CoinGecko / GeckoTerminal on-chain endpoints for token price, pool OHLCV, trades, and top-holder distribution where available.
- Chain explorer public holder pages or APIs for holder snapshots where available.
- Public social/search sources for mention counts and public media artifacts.

## GPT Referee Instruction

When using this template, the referee must classify each claim as confirmed, partly confirmed, not supported, or adjacent but different. Correlation is never causation unless the evidence supports the stronger claim.
