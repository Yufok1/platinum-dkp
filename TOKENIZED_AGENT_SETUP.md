# Tokenized Agent Setup

This file is the concrete setup path for a Platinum DKP tokenized agent.

There are two related surfaces:

1. Pump's Tokenized Agent setting for tokens, including agent deposit behavior and automated buyback/burn mechanics.
2. The `@pump-fun/agent-payments-sdk` flow for charging users for agent actions and verifying invoice payment on-chain.

Do not blur them. The setting is not magic AI. The SDK is a payment/invoice lane. Platinum DKP rules still control what the agent is allowed to sell, say, unlock, or score.

## Current Token

User-provided mint:

```text
F61Njyf8faE4NwrEmByWcdp8M56UHGeVaaQJPFGopump
```

Verify live before treating it as official.

## Decision Sheet

Fill this before writing code.

```text
Agent token mint:
Payment currency: USDC or SOL
Price amount in smallest unit:
RPC URL:
Framework: Next.js, Express, or other
What paid action unlocks:
What paid action does NOT unlock:
Where receipts are stored:
Human reviewer for disputes:
```

Smallest units:

```text
USDC: 1000000 = 1 USDC
SOL: 1000000000 = 1 SOL
```

Default public RPC options to choose from:

```text
https://rpc.solanatracker.io/public
https://rpc.ankr.com/solana
```

Do not silently pick one in code. Put it in environment variables.

## Allowed Paid Actions

Good paid actions:

- generate a quest draft
- submit a proposal for review
- create a lore card
- request a DKP receipt audit
- run a scam-link checklist
- format a governance proposal
- produce a public FAQ answer

Bad paid actions:

- buy/sell/hold advice
- price predictions
- pump planning
- wallet targeting
- seller harassment
- DKP for purchases
- treasury access
- private whale privileges
- guaranteed outcomes

Paid access buys a service request. It does not buy governance, DKP, treasury, or market advantage.

## Environment Variables

Use `.env.local` for Next.js or `.env` for Express.

```env
SOLANA_RPC_URL=https://rpc.solanatracker.io/public
NEXT_PUBLIC_SOLANA_RPC_URL=https://rpc.solanatracker.io/public
AGENT_TOKEN_MINT_ADDRESS=F61Njyf8faE4NwrEmByWcdp8M56UHGeVaaQJPFGopump

# USDC
CURRENCY_MINT=EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v

# Price in smallest unit. Example: 1 USDC.
PRICE_AMOUNT=1000000
```

For wrapped SOL instead:

```env
CURRENCY_MINT=So11111111111111111111111111111111111111112
PRICE_AMOUNT=1000000000
```

Never put private keys, seed phrases, wallet secrets, or treasury credentials in these files.

## Install

Check dependency ranges first:

```bash
npm info @pump-fun/agent-payments-sdk dependencies
```

Install the payment SDK and compatible Solana library:

```bash
npm install @pump-fun/agent-payments-sdk@3.0.2 @solana/web3.js@^1.98.0
```

For a browser wallet UI, install wallet adapter packages using versions compatible with the SDK dependency tree. Do not blindly install every latest package and then act surprised when the auction house catches fire.

## Server Flow

The server creates invoice parameters and builds an unsigned transaction.

Required invoice values:

```text
user wallet
currency mint
amount
memo
startTime
endTime
```

Rules:

- `amount > 0`
- `endTime > startTime`
- `amount`, `memo`, `startTime`, and `endTime` must match exactly during verification
- generate a unique numeric `memo` for every invoice
- verify payment server-side before delivering the service

## Client Flow

The client:

1. connects wallet
2. receives unsigned base64 transaction from server
3. deserializes it
4. asks wallet to sign
5. sends signed transaction
6. reports signature/result

The agent never signs for the user.

## Verification Flow

After the user signs and submits, the server verifies with the same invoice parameters.

Only deliver the paid service after verification returns true.

Use retries because chain confirmation is not instant:

```text
try verify
wait 2 seconds
repeat up to 10 times
fail closed if not verified
```

Fail closed means: no verified payment, no paid service. The loot window is not a suggestion box.

## Pump Tokenized Agent Setting Notes

Pump describes Tokenized Agent as a voluntary token setting. The setting lets certain automated smart contracts operate for tokens using it. Pump also states it is not itself AI.

Key behavior to understand before enabling:

- creators may upload a `skills.md` file at token creation
- agent deposit addresses can receive supported assets
- configured assets may be used for buyback and burn
- token buybacks occur according to creator-set parameters
- unused assets may be claimable by the token creator
- creators remain responsible for legal compliance and public statements

Because this touches token economics, publish clear disclosures. Do not imply guaranteed return, income, yield, treasury entitlement, or price support.

## Platinum DKP Guardrail

Every tokenized-agent action must still end with:

```text
Receipt
classification:
state:
rule:
evidence:
next_action:
```

If payment is involved:

```text
payment_status: verified | unverified | expired | rejected
invoice_id:
signature:
```

Do not expose full private user data in public receipts.

## Minimal Paid Action Menu

Start small:

```text
1 USDC - Quest Draft
1 USDC - Proposal Formatter
1 USDC - Scam Checklist
1 USDC - Receipt Audit Draft
```

Do not sell:

```text
DKP awards
governance votes
treasury claims
moderation immunity
market calls
whale access
```

## Preflight Checklist

- token mint verified
- currency selected
- smallest-unit price selected
- RPC selected
- framework selected
- environment variables configured
- wallet signing works
- server-side verification works
- duplicate invoice test passes
- expired invoice test passes
- failed payment does not deliver service
- market-talk policy wired into the agent
- treasury gate wired into the agent
- receipts appended to every output

