#!/usr/bin/env python3
"""
Example: Arc Integrity Integration Demo

Demonstrates the unified Fibonacci Bloom × Guardian-Arc verification system.
"""

import json
import hashlib
from typing import Dict, Any

import arc_integrity
import full_verifier


def sha3_json(obj: Any) -> str:
    """Deterministic SHA3-512 of JSON-serializable object."""
    blob = json.dumps(obj, separators=(",", ":"), sort_keys=True).encode()
    return hashlib.sha3_512(blob).hexdigest()


def generate_sample_envelope(n_coils: int = 13, genesis: str = "2025-12-02T23:59:59Z") -> Dict[str, Any]:
    """
    Generate a sample Fibonacci Bloom Integrity Envelope for demonstration.

    Args:
        n_coils: Number of Fibonacci coils to generate
        genesis: Genesis timestamp

    Returns:
        Valid Fibonacci Bloom Integrity Envelope
    """
    RESONANCE_HZ = 963

    # Generate Fibonacci coil chain
    fingerprints = []
    generations = []

    for i in range(n_coils):
        if i == 0:
            parent_a, parent_b = "0", "0"
        elif i == 1:
            parent_a, parent_b = "0", fingerprints[0]
        else:
            parent_a = fingerprints[i - 2]
            parent_b = fingerprints[i - 1]

        # Compute fingerprint
        seed = f"{parent_a}{parent_b}{genesis}{RESONANCE_HZ}".encode()
        fp = hashlib.sha3_512(seed).hexdigest()
        fingerprints.append(fp)

        generations.append({
            "coil": i,
            "fingerprint": fp,
            "parents": [parent_a[:8] + "..." if parent_a != "0" else "0",
                       parent_b[:8] + "..." if parent_b != "0" else "0"]
        })

    # Compute phi ratio from last two fingerprints
    if len(fingerprints) >= 2:
        f_n = int(fingerprints[-1][:16], 16)
        f_n1 = int(fingerprints[-2][:16], 16)
        phi_ratio = f_n / f_n1 if f_n1 != 0 else full_verifier.TRUE_PHI
    else:
        phi_ratio = full_verifier.TRUE_PHI

    # Build serpent_bloom_core
    bloom_core = {
        "genesis": genesis,
        "resonance_hz": RESONANCE_HZ,
        "generations": generations,
        "phi_ratio_observed": phi_ratio,
    }

    # Compute eternal fingerprint
    eternal_fp = sha3_json(bloom_core)
    bloom_core["eternal_fingerprint"] = eternal_fp

    # Build full envelope
    envelope = {
        "serpent_bloom_core": bloom_core,
        "external_fingerprints": [
            {
                "source": "example_generator",
                "algorithm": "SHA3-512",
                "value": eternal_fp
            }
        ]
    }

    return envelope


def demo_basic_integration():
    """Demonstrate basic Arc Integrity verification."""
    print("=" * 60)
    print("DEMO 1: Basic Arc Integrity Verification")
    print("=" * 60)

    # Generate sample envelope
    envelope = generate_sample_envelope(n_coils=13)

    # Verify with Arc
    print("\nVerifying envelope with Arc Integrity...\n")
    verification = arc_integrity.verify_with_arc(envelope, n_steps=500_000, bins=256)

    # Print verification result
    print(json.dumps(verification, indent=2))

    print("\n✓ Basic verification complete")
    print("=" * 60)


def demo_visualization():
    """Demonstrate Guardian-Arc visualization."""
    print("\n" + "=" * 60)
    print("DEMO 2: Guardian-Arc Visualization")
    print("=" * 60)

    # Generate sample envelope
    envelope = generate_sample_envelope(n_coils=21)

    print("\nGenerating Guardian-Arc visualization...")
    print("  - Extracting Fibonacci fingerprints")
    print("  - Seeding trajectory generator")
    print("  - Computing invariant density field ρ*")
    print("  - Rendering visualization...")

    # Create visualization
    fig = arc_integrity.visualize_integrity(
        envelope,
        n_steps=1_000_000,
        bins=384,
        blend_mode="composite",
        output_path="arc_integrity_demo.png",
        render_mode="density"
    )

    print("\n✓ Visualization saved to: arc_integrity_demo.png")
    print("=" * 60)


def demo_comparison():
    """Demonstrate envelope comparison."""
    print("\n" + "=" * 60)
    print("DEMO 3: Envelope Comparison")
    print("=" * 60)

    # Generate multiple envelopes with different characteristics
    envelopes = [
        generate_sample_envelope(n_coils=8),
        generate_sample_envelope(n_coils=13),
        generate_sample_envelope(n_coils=21),
    ]

    labels = ["8 Coils", "13 Coils", "21 Coils"]

    print("\nComparing envelopes with different Fibonacci depths...")
    print("  - Envelope 1: 8 coils (Fibonacci F8)")
    print("  - Envelope 2: 13 coils (Fibonacci F13)")
    print("  - Envelope 3: 21 coils (Fibonacci F21)")

    # Create comparison visualization
    fig = arc_integrity.compare_envelopes(
        envelopes,
        labels=labels,
        n_steps=500_000,
        bins=256,
        output_path="arc_comparison_demo.png"
    )

    print("\n✓ Comparison saved to: arc_comparison_demo.png")
    print("=" * 60)


def demo_seed_extraction():
    """Demonstrate fingerprint-to-seed conversion."""
    print("\n" + "=" * 60)
    print("DEMO 4: Fingerprint Seed Extraction")
    print("=" * 60)

    # Generate envelope
    envelope = generate_sample_envelope(n_coils=5)
    bloom_core = envelope["serpent_bloom_core"]

    print("\nExtracting seeds from Fibonacci fingerprints:\n")

    # Extract seeds
    seeds = arc_integrity.extract_fingerprint_seeds(bloom_core)

    for i, (gen, seed) in enumerate(zip(bloom_core["generations"], seeds)):
        fp = gen["fingerprint"]
        print(f"Coil {i}:")
        print(f"  Fingerprint: {fp[:32]}...")
        print(f"  Seed:        {seed:.15f}")
        print()

    # Show blended seed
    blended = arc_integrity.blend_seeds(seeds)
    print(f"Phi-weighted composite seed: {blended:.15f}")

    print("\n✓ Seed extraction complete")
    print("=" * 60)


def main():
    """Run all demonstration examples."""
    print("\n" + "█" * 60)
    print("█" + " " * 58 + "█")
    print("█" + "  ARC INTEGRITY: INTEGRATION DEMONSTRATION".center(58) + "█")
    print("█" + "  Guardian-Arc × Fibonacci Bloom".center(58) + "█")
    print("█" + " " * 58 + "█")
    print("█" * 60 + "\n")

    try:
        # Run demos
        demo_basic_integration()
        demo_seed_extraction()
        demo_visualization()
        demo_comparison()

        print("\n" + "█" * 60)
        print("█" + " " * 58 + "█")
        print("█" + "  ALL DEMONSTRATIONS COMPLETE".center(58) + "█")
        print("█" + " " * 58 + "█")
        print("█" * 60 + "\n")

        print("Generated files:")
        print("  - arc_integrity_demo.png")
        print("  - arc_comparison_demo.png")
        print()

    except Exception as e:
        print(f"\n✗ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
