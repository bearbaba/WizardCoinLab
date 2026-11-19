# 2026-11-19 — Voluntary-choice hypothesis (unverified)

## New candidate

`prompts/voluntary_choice_explicit_20261119.txt` is a direct, transparent voluntary-choice framing. It explicitly rejects role spoofing, loans, sales, audits and custody reframing. This is a distinct control-style hypothesis testing whether an honest acknowledgment of the wizard's prohibition can change its decision; no success is predicted.

## Evidence status

- Public v0.3.0 example uses `gl.eq_principle.prompt_comparative` and updates `self.have_coin = not parsed_result['give_coin']`.
- Studio-dev explorer displays many `ask_for_coin` calls, but `FINALIZED` or `Accepted` does not prove `give_coin=true` or a winning bounty.
- No live transaction, no model benchmark, and no wallet interaction were performed for this candidate.
- Do not recommend the candidate for Studio Next until it produces parseable `give_coin: true` consistently on at least two actual model families. Even then, offline success is not consensus proof.

## Next verification

Run the existing free local-model benchmark with this candidate, record each model and response independently, validate strict Boolean and JSON, and only then decide whether to pursue on-chain public read-only evidence. Avoid interpreting repeated temperature-zero runs as validator votes.

Sources: https://github.com/genlayerlabs/genlayer-studio/blob/main/examples/contracts/wizard_of_coin.py and https://docs.genlayer.com/developers/intelligent-contracts/tools/genlayer-studio.
