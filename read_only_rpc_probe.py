#!/usr/bin/env python3
"""Read-only GenLayer Studio Dev / Studio Next public contract inspection.

This program never signs anything, never submits transactions, does not connect wallets,
and uses only a hardcoded allowlist of four *read-only* JSON-RPC methods.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import urllib.error
import urllib.request
from pathlib import Path

RPC = "https://studio-dev.genlayer.com/api"
CONTRACT = "0x5f52cA60835b30F6B5716acF7FE52cAb25D7B1bD"
TX_IDS = [
    "0x7788248b60b05fa94b9bd0f6524f9b988ac84a57061ef10fc3d29d54bf5af43d",
    "0xb55422584a6f8597b6678ece88b8b7c7c57b0306c8c71fa9909815c4dbefbd04",
]
READ_METHODS = frozenset({
    "gen_getContractCode",
    "gen_getContractState",
    "gen_getTransactionData",
    "gen_getTransactionReceipt",
})

def rpc(method: str, params: list) -> dict:
    if method not in READ_METHODS:
        raise ValueError("RPC method prohibited: " + method)
    packet = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}
    request = urllib.request.Request(
        RPC,
        data=json.dumps(packet).encode("utf-8"),
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",  # JSON-RPC POST is used for READ-ONLY methods only
    )
    with urllib.request.urlopen(request, timeout=22) as response:
        result = json.load(response)
    return result

def call(method: str, params: list) -> dict:
    try:
        data = rpc(method, params)
        if data.get("error"):
            print(method, "ERROR", data["error"])
        else:
            print(method, "OK")
        return data
    except Exception as exc:
        print(method, "NETWORK ERROR", type(exc).__name__, str(exc)[:220])
        return {"error": {"type": type(exc).__name__, "message": str(exc)[:500]}}

def main() -> None:
    out = {
        "purpose": "Read-only research: not an onchain win, no wallet, no transaction submission",
        "rpc": RPC,
        "contract": CONTRACT,
        "transactions": {},
    }
    code = call("gen_getContractCode", [{"address": CONTRACT, "status": "finalized"}])
    source = code.get("result")
    if isinstance(source, str):
        try:
            raw = base64.b64decode(source, validate=True)
            decoded = raw.decode("utf-8")
            out["deployed_code"] = {
                "sha256": hashlib.sha256(raw).hexdigest(),
                "length": len(raw),
                "has_wizard_class": "WizardOfCoin" in decoded,
                "has_prompt_comparative": "prompt_comparative" in decoded,
                "has_strict_eq": "strict_eq" in decoded,
                "has_have_coin": "have_coin" in decoded,
                "source": decoded if len(decoded) < 100000 else decoded[:100000],
            }
            print("Deployed code", out["deployed_code"]["sha256"],
                  "WizardOfCoin", out["deployed_code"]["has_wizard_class"],
                  "prompt_comparative", out["deployed_code"]["has_prompt_comparative"],
                  "strict_eq", out["deployed_code"]["has_strict_eq"])
        except Exception as exc:
            out["deployed_code_error"] = repr(exc)
    else:
        out["deployed_code_error"] = code.get("error")

    state = call("gen_getContractState", [{"address": CONTRACT, "status": "finalized"}])
    st = state.get("result")
    if isinstance(st, str):
        out["current_state_hex"] = st[:20000]
        try:
            raw = bytes.fromhex(st.removeprefix("0x"))
            print("Current state hex bytes", len(raw), "trailing", raw[-64:].hex())
            out["state_byte_length"] = len(raw)
            out["state_ascii_printables"] = "".join(chr(b) if 32 <= b < 127 else "." for b in raw[:300])
        except ValueError:
            pass
    else:
        out["state_error"] = state.get("error")

    for txid in TX_IDS:
        row = {}
        for method in ("gen_getTransactionData", "gen_getTransactionReceipt"):
            response = call(method, [{"txId": txid}])
            value = response.get("result")
            if isinstance(value, dict):
                row[method] = {
                    k: value.get(k) for k in
                    ("id", "sender", "recipient", "statusName", "resultName",
                     "txExecutionResultName", "txCallData", "round",
                     "returnData", "leaderPublicData", "result", "txExecutionResult")
                    if k in value
                }
                print("TX", txid, method, "status", value.get("statusName"),
                      "execution", value.get("txExecutionResultName"),
                      "recipient", value.get("recipient"))
            else:
                row[method] = response
        out["transactions"][txid] = row

    # Optional public Explorer GET endpoints, discovered from the open-source
    # genlayer-studio backend/protocol_rpc/explorer/router.py. No wallet or writes.
    explorer_urls = [
        "https://studio-dev.genlayer.com/api/explorer/address/" + CONTRACT,
        "https://explorer-studio-dev.genlayer.com/api/explorer/address/" + CONTRACT,
        "https://studio-next.genlayer.com/api/explorer/address/" + CONTRACT,
        "https://explorer-studio-next.genlayer.com/api/explorer/address/" + CONTRACT,
        "https://studio-dev.genlayer.com/api/explorer/transactions/" + TX_IDS[0],
    ]
    out["explorer_get"] = {}
    for url in explorer_urls:
        try:
            req = urllib.request.Request(url, headers={"Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=12) as response:
                raw_json = response.read(1024 * 1024)
                item = {"http_status": response.status,
                        "content_type": response.headers.get("Content-Type"),
                        "byte_count_capped": len(raw_json)}
                try:
                    payload = json.loads(raw_json)
                    if isinstance(payload, dict):
                        item["top_level_keys"] = list(payload)[:20]
                        value = payload.get("contract_code")
                        if isinstance(value, str):
                            item["code_sha256"] = hashlib.sha256(value.encode("utf-8")).hexdigest()
                            item["code_matches_wizard"] = "WizardOfCoin" in value
                            item["code_matches_prompt_comparative"] = "prompt_comparative" in value
                        if isinstance(payload.get("transaction"), dict):
                            tx = payload["transaction"]
                            item["tx_status"] = tx.get("status")
                            item["tx_data_keys"] = list(tx.get("data", {}))[:20] if isinstance(tx.get("data"), dict) else []
                        if "state" in payload and isinstance(payload["state"], dict):
                            item["state_fields"] = list(payload["state"])
                except (ValueError, UnicodeDecodeError):
                    item["body_start"] = raw_json[:120].decode("utf-8", errors="replace")
                print("EXPLORER GET", url, "HTTP", item["http_status"],
                      "keys", item.get("top_level_keys"))
                out["explorer_get"][url] = item
        except Exception as exc:
            status = getattr(exc, "code", None)
            item = {"http_status": status, "error_type": type(exc).__name__,
                    "error": str(exc)[:250]}
            print("EXPLORER GET", url, "UNAVAILABLE", item)
            out["explorer_get"][url] = item

    Path("results").mkdir(exist_ok=True)
    output = Path("results/nov19_read_only_rpc.json")
    output.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print("SAVED:", output)
    if not out.get("deployed_code") and "current_state_hex" not in out:
        print("WARNING: RPC did not provide contract code or state; treat results as inconclusive.")

if __name__ == "__main__":
    main()
