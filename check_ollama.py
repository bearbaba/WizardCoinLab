#!/usr/bin/env python3
"""Local-only Ollama readiness check. No paid endpoints and no wallet calls."""
from __future__ import annotations
import json
import sys
import urllib.error
import urllib.request

URL = 'http://127.0.0.1:11434/api/tags'

def main() -> int:
    print('Checking local Ollama:', URL)
    try:
        with urllib.request.urlopen(URL, timeout=5) as response:
            data = json.load(response)
    except (OSError, TimeoutError, ValueError) as exc:
        print('Ollama is not reachable on localhost. Start Ollama first.')
        print('Details:', exc)
        return 1
    names = sorted(str(x.get('name')) for x in data.get('models', []) if x.get('name'))
    if not names:
        print('Ollama is running, but no local models are installed.')
        print('To install examples: ollama pull llama3.2')
        return 2
    print('Locally available models:')
    for name in names:
        print('  -', name)
    print('Choose installed names with --models model1,model2')
    return 0

if __name__ == '__main__':
    sys.exit(main())
