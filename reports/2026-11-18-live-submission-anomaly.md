# Studio Next submission anomaly — 2026-11-18

## Observations from the actual game interface

User tested the two best local-model candidates, after previously submitting many other prompts successfully.

| Candidate | Offline results | Live Studio Next observation |
| --- | --- | --- |
| `prompts/cross_family/01_original_two_examples.txt` | 6/6 valid `give_coin:true` across Qwen2.5:3b, Gemma3:4b, Phi3:mini | The wallet showed a confirmation; immediately after confirmation the game displayed **"Your wallet couldn't send it."** The user could find **no transaction hash**. |
| `prompts/cross_family/05_few_shot_four_cases.txt` | 5/6 valid `give_coin:true` | User reports this prompt also **could not be sent**. Exact error and TX existence for this second prompt were not separately confirmed. |

For the first prompt the wallet UI showed a failed transaction around 10:24 AM 2026-11-18 Vietnam time on **GenLayer Studio Dev**, with a displayed **0.1 GEN** and recipient abbreviated `0xb7278...fe575`. The 0.1 GEN value is UI data and **does not establish an actual debit**.

The user said older, mostly rejected prompts were submitted and evaluated normally.

## What this does and does not imply

- **There is no evidence of an accepted GenLayer consensus or a won prize.**
- The first attempt showed **no visible transaction hash**. It might have been rejected before broadcast or otherwise failed in the transaction path.
- A response from some *local* models with `give_coin:true` does **not** mean that Studio Next executed those validators or returned true.
- Hypotheses include RPC submission error, fee/gas-budget or estimation issues, frontend/SDK serialization, and contract simulation/consensus/JSON errors. They are **not yet distinguished**.
- GenLayer Studio Dev / Studio Next preview naming may be correct for the environment; do not infer an incorrect network from the label alone.
- The two prompts are each well under 1000 characters.

## Highest-value next diagnostic, no additional transaction needed

1. Record the actual **MetaMask error code and error.message** from the failed activity, if available.
2. If replicating only when the user chooses to, open browser developer tools (F12), inspect Console and Network RPC errors around the submit attempt. Look for `eth_sendRawTransaction`, `eth_estimateGas`, fee-estimate or GenLayer API errors. Save the **error code and message**, request type, and HTTP status. **Do not publish raw signed transactions, wallet secrets, or API tokens.**
3. Compare the failing request to one previously successful ask (timestamps and request types) without making extra game transactions.
4. If there is a genuine TX hash, inspect transaction status in Studio Dev Explorer, and do not assume a wallet failure is a win.

## Related benchmark

The larger-model GitHub Actions workflow run [44224048048](https://github.com/bearbaba/WizardCoinLab/actions/runs/44224048048) was cancelled during its model-evaluation step. **No Mistral 7B / Qwen 7B / Llama 8B win/loss conclusion should be claimed from it.**

### References
- [Original Wizard of Coin contract](https://github.com/genlayerlabs/genlayer-studio/blob/main/examples/contracts/wizard_of_coin.py)
- [Studio limitations](https://docs.genlayer.com/developers/intelligent-contracts/tools/genlayer-studio/limitations)
- [Transaction encoding and submission](https://docs.genlayer.com/understand-genlayer-protocol/core-concepts/transactions/transaction-encoding-serialization-and-signing)
