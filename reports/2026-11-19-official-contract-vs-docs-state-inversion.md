# 2026-11-19: official Wizard contract vs documentation — state inversion regression risk

## Sources verified directly from GitHub

- **Current public Studio contract (v0.3.0)**: https://github.com/genlayerlabs/genlayer-studio/blob/main/examples/contracts/wizard_of_coin.py
  - Contents blob SHA: `63a873a1cfc0970d56e4c08e8882df54b4a4b782`.
  - LLM result: `gl.eq_principle.prompt_comparative(get_wizard_answer, "The value of give_coin has to match")`
  - Validates: `assert isinstance(parsed_result["give_coin"], bool)`
  - State transition: `self.have_coin = not parsed_result["give_coin"]`
- **Published docs example (legacy)**: https://github.com/genlayerlabs/genlayer-docs/blob/main/pages/developers/intelligent-contracts/examples/wizard-of-coin.mdx
  - Contents blob SHA: `7a47e95feda85b42327e2bfcaa25951e9c27f445`.
  - `nondet()` extracts `dat["give_coin"]`.
  - Calls `gl.eq_principle.strict_eq(nondet)`.
  - State transition: `self.have_coin = result`.

## Why this changes the interpretation

For an initially held coin (`have_coin: true`), the same model response would produce different storage:

| Parsed `give_coin` | Legacy docs `have_coin = result` | Current v0.3.0 `have_coin = not give_coin` |
| --- | --- | --- |
| `false` (wizard refuses) | `false` (incorrectly appears to have no coin) | `true` (correctly retains coin) |
| `true` (wizard grants) | `true` (incorrectly still has coin) | `false` (correctly gives it away) |

This means a docs-based harness could spuriously call a refusal a win or invert the winning condition. A `FINALIZED` or `SUCCESS` transaction on its own says nothing about winning.

The **WizardCoinLab** offline harness mirrors the current v0.3.0 transition; it does *not* reproduce the legacy docs bug. A future test should specifically guard the mapping against accidental reversal.

## Critical uncertainty

The Explorer contract candidate `0x5f52cA60835b30F6B5716acF7FE52cAb25D7B1bD` is widely used for `ask_for_coin` calls, but **has not had its deployed code or storage independently retrieved** (GitHub runner read-only RPC and Explorer GET requests returned HTTP 403). We therefore **cannot assert** the Portal campaign's active deployment uses exactly this v0.3.0 code.

In the user's confirmed live attempt on 2026-11-19, the UI showed `The wizard kept the coin` after validators completed. This confirms the user didn't win that attempt, but doesn't expose the deployed source version.

## Research recommendation

1. Determine the *actual deployed contract code/version* from an authorized public read-only data source. Do not infer it solely from docs or source main branch, and do not bypass HTTP 403.
2. Continue searching for an exact public winning transaction with a full hash, request string, and state transition corroborated by Portal.
3. Prefer version-fidelity, calibration and provenance tests to another sweep of cosmetically different prompts on small local models.
4. No wallet connections, no contract writes, no test GEN, no paid service and no promise of a winning prompt.

No new Studio Next win or two-model `give_coin:true` candidate is documented by this report.
