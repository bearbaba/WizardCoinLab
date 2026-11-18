# Semantic-classification follow-up tests

Origin: `prompts/extended/16_literal_output_constraint.txt` returned parseable `give_coin: true` once on Qwen 2.5 3B, while Llama 3.2 3B returned false. This is a **single-model anomaly, not consensus**.

These twelve variants aim to determine whether confusing a text-classification task with the contract's real action flag produces a stable Boolean `true` across models. The first reproduces the original prompt verbatim. Two models × two rounds per prompt = 48 offline samples, none on chain.

Prompts are examples for an authorized game testing lab, not a winning claim.
