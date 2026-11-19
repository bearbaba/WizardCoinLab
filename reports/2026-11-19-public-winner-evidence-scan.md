# 2026-11-19 public-source winner scan — no verified current winning prompt

## What was checked

- Official Wizard of Coin v0.3.0 source: https://github.com/genlayerlabs/genlayer-studio/blob/main/examples/contracts/wizard_of_coin.py
- Official GenLayer announcement feed: https://t.me/s/genlayerofficial
- User-facing portal: https://portal.genlayer.foundation/wizard
- Web searches for 2026 Studio Next winner, exact prompt, 1,000 GLP payout, `give_coin: true`, state `have_coin: false`, contract/game transaction.
- Public community reports of participation and unsuccessful attempts: https://teapaw.org/theoneneeobari and https://teapawt.net/onargudel
- Historical 2024 Paris Blockchain Week winner mention: https://genlayer.com/es/blog/introducing-the-genlayer-simulator-a-testbed-for-developers

## Evidence quality

- The official contract contains `gl.eq_principle.prompt_comparative(..., "The value of give_coin has to match")`, followed by `json.loads` and `self.have_coin = not parsed_result["give_coin"]`. The only reliable proof of a win is a verified actual `give_coin: true` accepted by the deployed network and/or a confirmed state transition to `have_coin: false`.
- The official 2024 announcement mentions exactly one in-person successful adventurer at Paris Blockchain Week; it does **not disclose the text of a winning prompt** nor guarantee the current 2026 configuration is vulnerable in the same way.
- Recent social posts are about attempts and rewards; one community poster describes four **failed** approaches (staking, trust, philosophy, fake maintenance/state override) and says consensus returned `give_coin:false`; this is first-person unverified social evidence, *not* independently validated transaction data.
- Another public social poster claims 2,235 attempts and no wins (in a separate post 1,850+ attempts). These totals have **not** been independently checked and should **not** be presented as official network-wide statistics.
- No publicly verifiable **full transaction hash + exact request + post-state** proving a current Studio Next prize win was found in this pass.

## Updated research priorities

1. Do not pursue repeated speculative rewrites of failed direct persuasion, role spoofing, Unicode, self-reference, or sale/loan arguments just because an isolated small local LLM outputs true.
2. Continue *read-only* search for verifiable onchain/public evidence. A transaction marked FINALIZED is insufficient.
3. Use independent multi-family real LLM benchmarks only when a clearly differentiated technical hypothesis appears; judge validity of JSON and the actual bool. A local 6/6 classification result already failed on real Studio Next; calibrate model-to-validator transfer accordingly.
4. No live Studio Next submission, wallet connection, paid service, or test GEN. Do not claim or promise guaranteed victory.

## Observed background

Two recent local AI runs (Nov 19): [Unicode boundaries 0/36](2026-11-19-unicode-boundary-benchmark.md), [ownership/disposition 0/54](2026-11-19-disposition-benchmark.md). Public GitHub runner RPC and Explorer GET calls returned HTTP 403 ([read-only audit](2026-11-19-read-only-rpc-explorer-audit.md)); this is an access limitation, not a verdict.
