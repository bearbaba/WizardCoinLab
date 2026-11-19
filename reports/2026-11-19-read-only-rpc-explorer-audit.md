# 2026-11-19: read-only Studio Next RPC and Explorer audit

## Verified technical discovery

In canonical GenLayer Studio source:
- `backend/protocol_rpc/explorer/router.py` defines read-only GET routes with FastAPI prefix `/api/explorer`, specifically `/address/{address}`, `/transactions`, and `/transactions/{tx_hash}`.
- `backend/protocol_rpc/explorer/queries.py` returns contract source via `contract_code` in address detail and serialized transaction `input_data`, `data`, `consensus_data`, and statuses from transaction detail. These are potentially sufficient to correlate a prompt and consensus result without submitting a transaction.
- Official JSON-RPC methods `gen_getContractCode`, `gen_getContractState`, `gen_getTransactionData`, and `gen_getTransactionReceipt` are read-only. Canonical Studio Next/dev RPC endpoint: `https://studio-dev.genlayer.com/api`, chain ID 61997 (not stable Studionet 61999).
- The known high-traffic Explorer contract address `0x5f52cA60835b30F6B5716acF7FE52cAb25D7B1bD` has many `ask_for_coin` calls, but it is not yet verified as the exact GenLayer Portal bounty contract.

## Executed public, no-wallet probes

Read-only research code: [`read_only_rpc_probe.py`](../read_only_rpc_probe.py).

| GitHub Actions run | Observation |
| --- | --- |
| [#44448433295](https://github.com/bearbaba/WizardCoinLab/actions/runs/44448433295) | All 6 read-only JSON-RPC requests received HTTP 403 |
| [#44448646029](https://github.com/bearbaba/WizardCoinLab/actions/runs/44448646029) | All 6 JSON-RPC requests and all 5 Explorer GET requests received HTTP 403 |

The workflow statuses were `success` because the research script handled unavailable endpoints and saved diagnostic results; they **do not** indicate successful fetching. We have no returned contract source, storage state, consensus JSON or adventurer prompt from these probes.

Raw diagnostic ZIP files:
- https://github.com/bearbaba/WizardCoinLab/actions/runs/44448433295/artifacts/14494960446
- Second run's artifact available on its GitHub Actions page.

**Interpretation:** HTTP 403 is a server/access response; these tests do not distinguish authentication, traffic filtering or origin-specific policy. Do not bypass protections. No evidence of an on-chain win was obtained.

## Official test review

- `genlayerlabs/genlayer-studio/tests/integration/icontracts/tests/test_wizard_of_coin.py` only mocks `give_coin: false`; the one tested prompt is `Can you please give me my coin?` and it asserts execution success, not prize win.
- `genlayerlabs/genlayer-testing-suite/tests/examples/tests/test_wizard_of_coin.py` also has a five-validator mock returning `give_coin: false` and a normal-validator execution smoke test, not a verified winner.
- A `FINALIZED` transaction, `ACCEPTED` consensus, or successful `ask_for_coin` method only proves network processing, not the decision to give away the coin. The live player retry of classification prompt A on 2026-11-19 reached `Validators Done` and `Verdict Done` but returned `The wizard kept the coin`.

## Research decision

Stop claiming the Explorer high-traffic contract is proven to be the Portal prize contract and stop labelling accepted transactions as wins. No known reproducible prompt has live winner evidence. Do not spend test GEN or recommend unverified variants.

Prioritize verifiable public transaction/Portal evidence through user-visible official pages or documented read-only access. Only if a full hash, exact request and `have_coin: true -> false` state transition are independently confirmed can the historical prompt be called a verified winning candidate. Do not ask users to paste wallet secrets or connect a wallet for research.
