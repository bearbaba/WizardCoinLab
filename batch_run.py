#!/usr/bin/env python3
"""Test multiple distinct candidate prompts against local Ollama models.
No Studio transactions, no external API, no wallet access.
"""
from __future__ import annotations
import argparse
import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from wizard_lab import build_prompt, query_ollama, mock_response, parse_contract_result, examine

ROOT = Path(__file__).resolve().parent

def main():
    ap = argparse.ArgumentParser(description='Batch-test *.txt prompt candidates locally')
    ap.add_argument('--directory', type=Path, default=ROOT / 'prompts')
    ap.add_argument('--mode', choices=['mock', 'ollama'], default='mock')
    ap.add_argument('--mock-kind', choices=['reject', 'grant', 'invalid', 'duplicate', 'fenced'], default='reject')
    ap.add_argument('--models', default='llama3.2,qwen2.5:7b')
    ap.add_argument('--rounds', type=int, default=3)
    ap.add_argument('--temperature', type=float, default=0)
    ap.add_argument('--timeout', type=int, default=150)
    ap.add_argument('--output', type=Path, default=ROOT / 'results')
    args = ap.parse_args()
    if not (1 <= args.rounds <= 30):
        ap.error('--rounds must be 1 to 30')
    if not (0 <= args.temperature <= 2):
        ap.error('--temperature must be 0 to 2')
    files = sorted(args.directory.glob('*.txt'))
    if not files:
        ap.error('No *.txt prompt candidates found in ' + str(args.directory))
    names = ['mock-' + args.mock_kind] if args.mode == 'mock' else [m.strip() for m in args.models.split(',') if m.strip()]
    if not names:
        ap.error('No Ollama model names supplied')
    aggregate = []
    summaries = []
    for filename in files:
        request = filename.read_text(encoding='utf-8-sig').strip()
        if not request or len(request) > 1000:
            print(f'SKIP: {filename.name} (empty or > 1000 characters)', file=sys.stderr)
            continue
        rows = []
        prompt = build_prompt(request)
        for name in names:
            for run in range(1, args.rounds + 1):
                try:
                    raw = mock_response(args.mock_kind) if args.mode == 'mock' else query_ollama(name, prompt, 'http://127.0.0.1:11434', args.timeout, args.temperature)
                    result = parse_contract_result(raw)
                except Exception as exc:
                    raw = ''
                    result = {'valid': False, 'give_coin': None, 'have_coin_after': None, 'reasoning': '', 'duplicate_keys': [], 'error': str(exc)}
                item = {
                    'candidate': filename.name, 'model': name, 'run': run,
                    **result, 'raw_response': raw,
                }
                rows.append(item)
                aggregate.append(item)
        summary = examine(rows)
        summaries.append({'candidate': filename.name, **summary})
        print(f"{filename.name:<32} true={summary['true']}/{summary['samples']} valid={summary['valid_json']} all_true_heuristic={summary['all_true_strict_heuristic']}")
    args.output.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
    fname = args.output / f'batch_{ts}.json'
    fname.write_text(json.dumps({'mode': args.mode, 'summaries': summaries, 'rows': aggregate,
        'warning': 'All results are offline; mock is a parser fixture, Ollama is not Studio Next or GenLayer consensus'},
        indent=2, ensure_ascii=False), encoding='utf-8')
    csvpath = fname.with_suffix('.csv')
    with csvpath.open('w', encoding='utf-8-sig', newline='') as out:
        writer = csv.DictWriter(out, fieldnames=['candidate','samples','valid_json','true','false','all_agree_strict_heuristic','all_true_strict_heuristic'])
        writer.writeheader()
        for s in summaries:
            writer.writerow({k:s.get(k) for k in writer.fieldnames})
    print('SAVED:', fname)
    print('SAVED:', csvpath)
    if args.mode == 'mock':
        print('CAUTION: Mock does not ask an AI. The same hardcoded response is returned to every candidate.')
    else:
        print('CAUTION: Ollama runs are independent local model samples, not network validators.')

if __name__ == '__main__':
    main()
