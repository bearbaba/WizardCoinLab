# WizardCoinLab

**Offline Wizard of Coin testing kit — no wallet, no Studio Next transaction, no test GEN.**

This independent Python lab reproduces the *public* Wizard of Coin v0.3.0 prompt structure, JSON parsing behavior, and `have_coin` transition. It is **not** an official GenLayer app, validator, or prize oracle. Offline model agreement does **not** prove GenLayer network consensus.

## Requirements

- Windows, macOS, or Linux; Python 3.10+
- No Python packages to install
- Optional: [Ollama](https://ollama.com/download) and local AI models for actual local language-model tests

## Run built-in tests

```powershell
python -m unittest discover -s tests -v
python wizard_lab.py --mode mock --mock-kind reject --rounds 3
python wizard_lab.py --mode mock --mock-kind grant --rounds 3
python wizard_lab.py --mode mock --mock-kind duplicate --rounds 1
python batch_run.py --mode mock --rounds 3
```

Mock responses are predefined parser fixtures: a mock `true` is **not** a successful persuasive prompt.

## Test with local AI (free, optional)

Install Ollama; download models:

```powershell
ollama pull llama3.2
ollama pull qwen2.5:7b
```

Edit `prompts/candidate.txt` (at most 1000 characters), then:

```powershell
python wizard_lab.py --mode ollama --models llama3.2,qwen2.5:7b --rounds 3
python batch_run.py --mode ollama --models llama3.2,qwen2.5:7b --rounds 3
```

Ollama must be running locally on port 11434. Results are saved as JSON and CSV under the ignored `results/` directory. No wallet or paid API is needed. Local model responses will not necessarily match the actual GenLayer AI validators.

## How to interpret outcomes

- `give_coin: true` => reconstructed contract transition `have_coin = False`
- `give_coin: false` => reconstructed contract transition `have_coin = True`
- `valid=false` => the response failed JSON or Boolean validation
- `duplicate_keys` => reported diagnostic; Python `json.loads` keeps the last duplicate value
- `all_true_strict_heuristic` => every local test sample returned valid `true` — **not** an on-chain verdict

The real contract uses GenLayer's `gl.eq_principle.prompt_comparative(...)`, which is *not* reproduced by this heuristic. Every individual test starts with `have_coin: True`.

Inspect the full prompt assembled by this kit:

```powershell
python wizard_lab.py --mode mock --print-full-prompt --rounds 1
```

Only paste the adventurer message in `prompts/candidate.txt` into the game interface; never paste the full reconstructed contract prompt.

## GenLayer Studio local (separate, optional)

To test the actual Intelligent Contract and local validators, follow official [GenLayer tooling setup](https://docs.genlayer.com/developers/intelligent-contracts/tooling-setup) with Docker and Node.js. Typical commands:

```powershell
npm install -g genlayer
genlayer init
genlayer up
```

Then open `http://localhost:8080`, import the official contract, and configure local validators and model providers. That setup may require credentials or carry provider costs. It has **not** been executed by the author of this testing kit.

## Sources

- [GenLayer Wizard of Coin public contract](https://github.com/genlayerlabs/genlayer-studio/blob/main/examples/contracts/wizard_of_coin.py)
- [GenLayer tooling setup](https://docs.genlayer.com/developers/intelligent-contracts/tooling-setup)
- [GenLayer Studio](https://docs.genlayer.com/developers/intelligent-contracts/tools/genlayer-studio)

For education and local testing only. This project is independent of GenLayer.
## Improvements — prompt fidelity and automated checks

The reconstructed prompt now matches the public GenLayer v0.3.0 source **byte-for-byte after interpolation**, including whitespace and newlines. The exact expected text is in tests/fixtures/prompt_v030_expected.txt.

GitHub Actions runs Python 3.10, 3.12, and 3.13 unit tests and mock smoke tests on every push to main and every pull request. CI never downloads AI models, reaches Studio Next, or uses wallet keys.

On Windows you can double-click run_ollama_windows.bat for a local installation check. It never pulls models automatically. You can run python check_ollama.py and then python batch_run.py --mode ollama --models llama3.2,qwen2.5:7b --rounds 3.

**Important:** Mock mode tests parsing only; it does not rank prompts. Local Ollama performance is exploratory, not evidence of Studio Next victory or of network validator agreement.
