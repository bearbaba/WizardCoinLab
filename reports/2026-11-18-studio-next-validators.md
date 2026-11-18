# Studio Next validator model landscape (observed 2026-11-18)

Reference: https://explorer-studio-next.genlayer.com/validators

At the time of inspection the public Studio Next Explorer listed **16 active validators** with **2 provider labels**; visible model/configuration names included:

- llm-router / policy:dev-gpt-5-4 (3)
- llm-router / policy:dev-gemini (2)
- llm-router / policy:dev-sonnet (2)
- llm-router / policy:dev-deepseek (2)
- llm-router / policy:dev-gpt-oss (1)
- llm-router / policy:dev-grok (1)
- llm-router / policy:dev-mistral (1)
- openrouter / openai/gpt-5.4 (2)
- openrouter / anthropic/claude-sonnet-4.6 (1)
- openrouter / google/gemini-3-flash-preview (1)

These are *labels from the Explorer*, not independent proof of the exact backend versions used in any historical Wizard of Coin transaction. Validator composition may change.

### Implications for WizardCoinLab

1. Our local Ollama models (`qwen2.5:3b`, `llama3.2:3b`, `gemma3:4b`, `phi3:mini`) **do not reproduce these live validators**. Treat them as inexpensive probes for possible instruction confusion only.
2. A local `give_coin:true` is especially weak if it appears on just one small model. Neither a mocked result nor a single-model error is a confirmed prize-winning exploit.
3. Do not transmit a prompt on Studio Next solely because Qwen showed `true`. Higher-confidence evidence would be independent responses from frontier-style model families and/or a verifiable on-chain win.
4. Avoid paid APIs and test GEN unless the user separately opts in.

More docs: https://docs.genlayer.com/developers/intelligent-contracts/tools/genlayer-studio/providers
