#!/usr/bin/env python3
"""
Fibonacci Bloom Integrity — Full Verifier (Serpent × Inverse Pegasus)

Validates:
  1. Eternal fingerprint
     - SHA3-512 over serpent_bloom_core, excluding eternal_fingerprint itself
  2. Fibonacci coil chain
     - Coil 0: hash("0", "0", genesis, RESONANCE_HZ)
     - Coil 1: hash("0", fp_0, genesis, RESONANCE_HZ)
     - Coil n: hash(fp_(n-2), fp_(n-1), genesis, RESONANCE_HZ)
  3. Phi ratio
     - |phi_ratio_observed - φ| < PHI_TOL
  4. External fingerprints
     - Count, sources, algorithms (stubbed for future MITM recompute)
"""

import json
import hashlib
import sys
from pathlib import Path
from typing import Dict, Any, Tuple, List

# ─────────────────────────────────────────────────────────
# CONSTANTS — must match generator
# ─────────────────────────────────────────────────────────

GENESIS_TIMESTAMP = "2025-12-02T23:59:59Z"
RESONANCE_HZ = 963
TRUE_PHI = (1 + 5 ** 0.5) / 2  # 1.6180339887498948...
PHI_TOL = 1e-9  # numerical stability allowance for float serialization

HEX_CHARS = set("0123456789abcdefABCDEF")


# ─────────────────────────────────────────────────────────
# CORE HASH FUNCTIONS
# ─────────────────────────────────────────────────────────

def sha3_512_hex(data: bytes) -> str:
    """SHA3-512 of raw bytes → lowercase hex string."""
    return hashlib.sha3_512(data).hexdigest()


def sha3_json(obj: Any) -> str:
    """Deterministic SHA3-512 of JSON-serializable object."""
    blob = json.dumps(obj, separators=(",", ":"), sort_keys=True).encode()
    return sha3_512_hex(blob)


def fibonacci_fingerprint(genesis: str, parent_a: str, parent_b: str) -> str:
    """
    Compute fingerprint matching the generator’s algorithm:

        seed = f"{parent_a}{parent_b}{genesis}{RESONANCE_HZ}".encode()
        return sha3_512_hex(seed)
    """
    seed = f"{parent_a}{parent_b}{genesis}{RESONANCE_HZ}".encode()
    return sha3_512_hex(seed)


def is_valid_sha3_hex(s: str) -> bool:
    """Check if s is a valid SHA3-512 hex string (128 hex chars)."""
    return isinstance(s, str) and len(s) == 128 and all(c in HEX_CHARS for c in s)


# ─────────────────────────────────────────────────────────
# VERIFICATION FUNCTIONS
# ─────────────────────────────────────────────────────────

def verify_eternal_fingerprint(bloom_core: Dict[str, Any]) -> Tuple[bool, str, str]:
    """
    Verify eternal_fingerprint by recomputing SHA3-512 over serpent_bloom_core,
    excluding eternal_fingerprint itself.

    Returns:
        (ok, stored_value, recomputed_value)
    """
    temp = dict(bloom_core)
    stored = temp.pop("eternal_fingerprint", None)
    recomputed = sha3_json(temp)
    return (stored == recomputed), (stored or ""), recomputed


def verify_coil_chain(
    bloom_core: Dict[str, Any]
) -> Tuple[bool, List[int], List[Dict[str, Any]]]:
    """
    Verify Fibonacci fingerprint chain:

      - Coil indices must be contiguous 0..N-1
      - Coil 0: hash("0", "0", genesis)
      - Coil 1: hash("0", fp_0, genesis)
      - Coil n: hash(fp_(n-2), fp_(n-1), genesis)

    Returns:
        (all_ok, bad_coil_indices, details_list)
    """
    generations = bloom_core.get("generations", [])
    genesis = bloom_core.get("genesis", GENESIS_TIMESTAMP)

    if not generations:
        return True, [], []

    bad_coils: List[int] = []
    details: List[Dict[str, Any]] = []
    fingerprints: List[str] = []

    for i, gen in enumerate(generations):
        idx = gen.get("coil", i)
        stored_fp = gen.get("fingerprint", "")

        # Index sanity: require contiguous 0..N-1
        if idx != i:
            bad_coils.append(idx)
            details.append({
                "coil": idx,
                "error": "index_mismatch",
                "expected_index": i,
                "actual_index": idx,
            })

        # Validate fingerprint format
        if not is_valid_sha3_hex(stored_fp):
            bad_coils.append(idx)
            details.append({
                "coil": idx,
                "error": "invalid_fingerprint_format",
                "expected_length": 128,
                "actual_length": len(stored_fp),
            })
            fingerprints.append(stored_fp)
            continue

        # Parents driven by position, not label
        if i == 0:
            parent_a, parent_b = "0", "0"
        elif i == 1:
            parent_a, parent_b = "0", fingerprints[0]
        else:
            parent_a = fingerprints[i - 2]
            parent_b = fingerprints[i - 1]

        expected_fp = fibonacci_fingerprint(genesis, parent_a, parent_b)

        if stored_fp != expected_fp:
            bad_coils.append(idx)
            details.append({
                "coil": idx,
                "error": "fingerprint_mismatch",
                "expected": expected_fp[:32] + "...",
                "actual": stored_fp[:32] + "...",
            })

        fingerprints.append(stored_fp)

    return len(bad_coils) == 0, bad_coils, details


def verify_phi(bloom_core: Dict[str, Any]) -> Tuple[bool, float, float]:
    """
    Verify phi ratio matches true golden ratio within tolerance PHI_TOL.

    Returns:
        (ok, observed_phi, delta)
    """
    observed = bloom_core.get("phi_ratio_observed", 0.0)
    delta = abs(observed - TRUE_PHI)
    return delta < PHI_TOL, observed, delta


def verify_external_fingerprints(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Verify external_fingerprints block.

    For design-spec mode:
      - Only reports count, sources, algorithms.
      - 'verified' is reserved for future MITM recompute.
    """
    externals = data.get("external_fingerprints", [])

    return {
        "count": len(externals),
        "sources": [e.get("source") for e in externals],
        "algorithms": [e.get("algorithm") for e in externals],
        "verified": None  # placeholder for future external hash verification
    }


def verify_envelope(data: Dict[str, Any]) -> Dict[str, Any]:
    """Full envelope verification for Fibonacci Bloom Integrity Envelope."""
    bloom_core = data.get("serpent_bloom_core", {})

    # Eternal fingerprint
    ef_ok, stored_ef, recomputed_ef = verify_eternal_fingerprint(bloom_core)

    # Coil chain
    chain_ok, bad_coils, chain_details = verify_coil_chain(bloom_core)

    # Phi ratio
    phi_ok, phi_observed, phi_delta = verify_phi(bloom_core)

    # External fingerprints
    external_report = verify_external_fingerprints(data)

    # Overall verdict
    all_ok = ef_ok and chain_ok and phi_ok

    return {
        "verification_result": "PASS" if all_ok else "FAIL",
        "eternal_fingerprint": {
            "ok": ef_ok,
            "stored": stored_ef[:32] + "..." if stored_ef else None,
            "recomputed": recomputed_ef[:32] + "..."
        },
        "coil_chain": {
            "ok": chain_ok,
            "coils_checked": len(bloom_core.get("generations", [])),
            "bad_coils": bad_coils,
            "details": chain_details or None,
        },
        "phi_ratio": {
            "ok": phi_ok,
            "observed": phi_observed,
            "expected": TRUE_PHI,
            "delta": phi_delta,
            "tolerance": PHI_TOL,
        },
        "external_fingerprints": external_report,
        "verdict": (
            "Envelope cryptographically consistent — all checks passed"
            if all_ok else
            "Envelope has integrity issues — see details above"
        ),
    }


# ─────────────────────────────────────────────────────────
# CLI ENTRYPOINT
# ─────────────────────────────────────────────────────────

def main() -> None:
    # 1) Explicit file via argv
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
        try:
            data = json.loads(path.read_text())
        except json.JSONDecodeError as e:
            print(f"JSON error in {path}: {e}", file=sys.stderr)
            sys.exit(1)
        print(json.dumps(verify_envelope(data), indent=2))
        return

    # 2) JSON piped via stdin
    if not sys.stdin.isatty():
        try:
            data = json.load(sys.stdin)
        except json.JSONDecodeError as e:
            print(f"JSON error on stdin: {e}", file=sys.stderr)
            sys.exit(1)
        print(json.dumps(verify_envelope(data), indent=2))
        return

    # 3) Fallback: common filenames / mounts
    candidates = [
        Path("/mnt/user-data/uploads/fibonacci_bloom_envelope.json"),
        Path("/mnt/data/fibonacci_bloom_envelope.json"),
        Path("fibonacci_bloom_envelope.json"),
        Path("correct_envelope.json"),
    ]
    path = next((p for p in candidates if p.exists()), None)
    if not path:
        print("Usage: python full_verifier.py <envelope.json>")
        print("   or: cat envelope.json | python full_verifier.py")
        sys.exit(1)

    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        print(f"JSON error in {path}: {e}", file=sys.stderr)
        sys.exit(1)

    report = verify_envelope(data)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()