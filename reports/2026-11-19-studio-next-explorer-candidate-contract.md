# Explorer discovery for Wizard of Coin: live contract candidate, NOT a verified winning prompt

Date: 2026-11-19 UTC; manual public explorer/web search; no wallet, no Studio tx, no paid API.

## Candidate live contract

Public Studio Next explorer address:

https://explorer-studio-next.genlayer.com/address/0x5f52cA60835b30F6B5716acF7FE52cAb25D7B1bD

- Exact address: `0x5f52cA60835b30F6B5716acF7FE52cAb25D7B1bD`.
- Explorer displays thousands of `ask_for_coin` method calls to this address from many accounts. One public page response showed 3,612 total transactions, and a subsequent response showed 4,547; counts are dynamic and/or crawler time-dependent.
- Explorer lists deployment on 2026-11-16, and numerous `FINALIZED` calls with GenVM `SUCCESS` and consensus `Accepted`.
- **Crucial:** `Accepted` / `FINALIZED` / `SUCCESS` indicate transaction execution and consensus accepted, **not** that the Wizard gave away the coin. The contract may run successfully with `give_coin:false`.
- We have **not independently proven** that this is exactly the Portal bounty campaign contract rather than a related public contract. Do not label it as official bounty contract without confirming the portal address.
- The public explorer's full address page lists transaction hashes as clickable items, but the few transaction detail fetches attempted returned a thin client-rendered shell, not enough verified calldata, LLM JSON, or changed `have_coin` state to declare any win.

## Next verification route

1. Confirm the contract address from the actual Portal Wizard game (read-only page source or authenticated user-visible link) before tying it to bounties.
2. Retrieve a complete `ask_for_coin` transaction hash and both the adventurer's input and consensus result via the supported explorer/API, with provenance. No transaction submissions.
3. Read the contract state before/after for a verified `have_coin: true -> false` transition. A finalized call alone is not a win.
4. If a winning transaction is found, cross-check the exact prompt and changed state on two independently observable sources before recommending any replay.
5. Keep the actual contract's current source/version separated from the older docs example using `strict_eq`, which differs from current `prompt_comparative`.

## Search notes

Public web searches for a Studio Next winning prompt on 2026-11-19 surfaced unverified forum/social anecdotes and several **documented losing** strategies, but no full-hash, exact-text, state-verified winning prompt. The known 2024 Paris Blockchain Week historic winner mentioned by GenLayer does not supply its prompt or establish modern game behavior.

This is a research lead, **not** evidence that anyone won the current bounty.
