#!/usr/bin/env python3
"""
Arc Integrity — Guardian-Arc × Fibonacci Bloom Integration

Combines cryptographic verification with visual density field analysis:
  - Fibonacci fingerprints seed Guardian-Arc trajectories
  - Visual patterns reveal structural integrity
  - Unified verification with both numerical and geometric validation
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

# Import core modules
import full_verifier
import guardian_arc


def fingerprint_to_seed(fingerprint: str) -> float:
    """
    Convert SHA3-512 hex fingerprint to a float seed in [0, 1).

    Uses first 16 hex chars for numerical stability.
    """
    if not fingerprint or len(fingerprint) < 16:
        return 0.123456789  # default seed

    # Take first 16 hex chars (64 bits)
    hex_segment = fingerprint[:16]
    int_val = int(hex_segment, 16)
    # Normalize to [0, 1)
    return (int_val % (2**53)) / (2**53)


def extract_fingerprint_seeds(bloom_core: Dict[str, Any]) -> List[float]:
    """
    Extract all Fibonacci coil fingerprints and convert to seeds.
    """
    generations = bloom_core.get("generations", [])
    seeds = []

    for gen in generations:
        fp = gen.get("fingerprint", "")
        if full_verifier.is_valid_sha3_hex(fp):
            seeds.append(fingerprint_to_seed(fp))

    return seeds


def blend_seeds(seeds: List[float]) -> float:
    """
    Blend multiple seeds into a single composite seed using phi-weighted sum.
    """
    if not seeds:
        return 0.123456789

    if len(seeds) == 1:
        return seeds[0]

    # Phi-weighted blend
    phi = guardian_arc.phi
    weights = np.array([phi ** (-i) for i in range(len(seeds))])
    weights /= weights.sum()

    blended = sum(w * s for w, s in zip(weights, seeds))
    return float(blended % 1.0)


def integrity_trajectory(
    bloom_core: Dict[str, Any],
    n_steps: int = 2_000_000,
    burn_in: int = 1_000,
    blend_mode: str = "composite"
) -> np.ndarray:
    """
    Generate Guardian-Arc trajectory seeded by Fibonacci fingerprints.

    Args:
        bloom_core: The serpent_bloom_core from envelope
        n_steps: Number of trajectory steps
        burn_in: Initial steps to discard
        blend_mode: "composite" (blend all seeds) or "first" (use first coil only)

    Returns:
        Complex trajectory array
    """
    seeds = extract_fingerprint_seeds(bloom_core)

    if blend_mode == "composite":
        seed = blend_seeds(seeds)
    elif blend_mode == "first" and seeds:
        seed = seeds[0]
    else:
        seed = 0.123456789  # fallback

    return guardian_arc.guardian_arc_trajectory(
        n_steps=n_steps,
        burn_in=burn_in,
        seed=seed
    )


def verify_with_arc(
    data: Dict[str, Any],
    n_steps: int = 2_000_000,
    bins: int = 512,
    blend_mode: str = "composite"
) -> Dict[str, Any]:
    """
    Full verification with Guardian-Arc trajectory generation.

    Returns:
        Combined report with verification + trajectory metadata
    """
    # Standard verification
    verification = full_verifier.verify_envelope(data)

    # Generate Arc trajectory
    bloom_core = data.get("serpent_bloom_core", {})
    seeds = extract_fingerprint_seeds(bloom_core)
    trajectory = integrity_trajectory(bloom_core, n_steps=n_steps, blend_mode=blend_mode)

    # Add Arc metadata to report
    verification["guardian_arc"] = {
        "trajectory_steps": len(trajectory),
        "seeds_extracted": len(seeds),
        "blend_mode": blend_mode,
        "seed_used": blend_seeds(seeds) if blend_mode == "composite" else (seeds[0] if seeds else 0.123456789),
        "trajectory_bounds": {
            "real_min": float(trajectory.real.min()),
            "real_max": float(trajectory.real.max()),
            "imag_min": float(trajectory.imag.min()),
            "imag_max": float(trajectory.imag.max()),
        }
    }

    return verification


def visualize_integrity(
    data: Dict[str, Any],
    n_steps: int = 2_000_000,
    bins: int = 512,
    blend_mode: str = "composite",
    output_path: Optional[str] = None,
    render_mode: str = "density"
) -> plt.Figure:
    """
    Create integrated visualization showing verification + density field.

    Args:
        data: Fibonacci Bloom Integrity Envelope
        n_steps: Trajectory steps
        bins: Density grid resolution
        blend_mode: Seed blending strategy
        output_path: Optional path to save figure
        render_mode: "density" or "hexbin"

    Returns:
        Matplotlib figure
    """
    # Verify and generate trajectory
    verification = verify_with_arc(data, n_steps=n_steps, bins=bins, blend_mode=blend_mode)
    bloom_core = data.get("serpent_bloom_core", {})
    trajectory = integrity_trajectory(bloom_core, n_steps=n_steps, blend_mode=blend_mode)

    # Create figure with two subplots
    fig, (ax_verify, ax_arc) = plt.subplots(1, 2, figsize=(16, 8))

    # Left panel: Verification summary
    ax_verify.axis('off')

    result = verification["verification_result"]
    result_color = "green" if result == "PASS" else "red"

    summary_text = f"""
FIBONACCI BLOOM INTEGRITY
{'=' * 40}

Status: {result}

Eternal Fingerprint: {'✓' if verification['eternal_fingerprint']['ok'] else '✗'}
  {verification['eternal_fingerprint']['recomputed']}

Coil Chain: {'✓' if verification['coil_chain']['ok'] else '✗'}
  Coils checked: {verification['coil_chain']['coils_checked']}
  Bad coils: {len(verification['coil_chain']['bad_coils'])}

Phi Ratio: {'✓' if verification['phi_ratio']['ok'] else '✗'}
  Observed: {verification['phi_ratio']['observed']:.15f}
  Expected: {verification['phi_ratio']['expected']:.15f}
  Delta: {verification['phi_ratio']['delta']:.2e}

External Fingerprints:
  Count: {verification['external_fingerprints']['count']}

{'=' * 40}
GUARDIAN-ARC INTEGRATION
{'=' * 40}

Trajectory steps: {verification['guardian_arc']['trajectory_steps']:,}
Seeds extracted: {verification['guardian_arc']['seeds_extracted']}
Blend mode: {verification['guardian_arc']['blend_mode']}
Seed value: {verification['guardian_arc']['seed_used']:.15f}

Bounds:
  Real: [{verification['guardian_arc']['trajectory_bounds']['real_min']:.3f}, {verification['guardian_arc']['trajectory_bounds']['real_max']:.3f}]
  Imag: [{verification['guardian_arc']['trajectory_bounds']['imag_min']:.3f}, {verification['guardian_arc']['trajectory_bounds']['imag_max']:.3f}]
    """

    ax_verify.text(
        0.05, 0.95, summary_text,
        transform=ax_verify.transAxes,
        fontfamily='monospace',
        fontsize=9,
        verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor=result_color, alpha=0.1)
    )

    # Right panel: Guardian-Arc density field
    if render_mode == "density":
        density, x_edges, y_edges = guardian_arc.guardian_arc_density(
            trajectory, bins=bins
        )
        guardian_arc.guardian_arc_plot(
            density, x_edges, y_edges, ax=ax_arc, cmap="inferno"
        )
    elif render_mode == "hexbin":
        guardian_arc.guardian_arc_hexbin(
            trajectory, gridsize=400, ax=ax_arc, cmap="inferno"
        )

    # Update title with verification result
    ax_arc.set_title(
        f"GUARDIAN-ARC vΩ\nInvariant Density ρ*\n[{result}]",
        fontsize=12,
        color=result_color
    )

    fig.suptitle(
        "Arc Integrity: Fibonacci Bloom × Guardian-Arc Unified Verification",
        fontsize=14,
        fontweight='bold'
    )

    plt.tight_layout()

    if output_path:
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Visualization saved to: {output_path}")

    return fig


def compare_envelopes(
    envelopes: List[Dict[str, Any]],
    labels: Optional[List[str]] = None,
    n_steps: int = 1_000_000,
    bins: int = 384,
    output_path: Optional[str] = None
) -> plt.Figure:
    """
    Compare multiple envelopes side-by-side with Guardian-Arc visualizations.

    Args:
        envelopes: List of Fibonacci Bloom Integrity Envelopes
        labels: Optional labels for each envelope
        n_steps: Trajectory steps
        bins: Density grid resolution
        output_path: Optional path to save figure

    Returns:
        Matplotlib figure
    """
    n_envelopes = len(envelopes)
    if labels is None:
        labels = [f"Envelope {i+1}" for i in range(n_envelopes)]

    fig, axes = plt.subplots(1, n_envelopes, figsize=(8 * n_envelopes, 10))
    if n_envelopes == 1:
        axes = [axes]

    for i, (envelope, label) in enumerate(zip(envelopes, labels)):
        verification = verify_with_arc(envelope, n_steps=n_steps, bins=bins)
        bloom_core = envelope.get("serpent_bloom_core", {})
        trajectory = integrity_trajectory(bloom_core, n_steps=n_steps)

        # Render density field
        density, x_edges, y_edges = guardian_arc.guardian_arc_density(
            trajectory, bins=bins
        )
        guardian_arc.guardian_arc_plot(
            density, x_edges, y_edges, ax=axes[i], cmap="inferno"
        )

        # Update title
        result = verification["verification_result"]
        result_color = "green" if result == "PASS" else "red"
        axes[i].set_title(
            f"{label}\n[{result}]",
            fontsize=12,
            color=result_color
        )

    fig.suptitle(
        "Guardian-Arc Envelope Comparison",
        fontsize=14,
        fontweight='bold'
    )

    plt.tight_layout()

    if output_path:
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Comparison saved to: {output_path}")

    return fig


def main() -> None:
    """CLI entrypoint for integrated Arc Integrity verification."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Arc Integrity: Fibonacci Bloom × Guardian-Arc unified verification"
    )
    parser.add_argument(
        "envelope",
        nargs="?",
        help="Path to Fibonacci Bloom Integrity Envelope JSON"
    )
    parser.add_argument(
        "--visualize", "-v",
        action="store_true",
        help="Generate Guardian-Arc visualization"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output path for visualization (PNG)"
    )
    parser.add_argument(
        "--steps", "-s",
        type=int,
        default=2_000_000,
        help="Trajectory steps (default: 2,000,000)"
    )
    parser.add_argument(
        "--bins", "-b",
        type=int,
        default=512,
        help="Density grid resolution (default: 512)"
    )
    parser.add_argument(
        "--blend-mode", "-m",
        choices=["composite", "first"],
        default="composite",
        help="Seed blending mode (default: composite)"
    )
    parser.add_argument(
        "--render-mode", "-r",
        choices=["density", "hexbin"],
        default="density",
        help="Rendering mode (default: density)"
    )

    args = parser.parse_args()

    # Load envelope
    if args.envelope:
        path = Path(args.envelope)
    elif not sys.stdin.isatty():
        # Read from stdin
        try:
            data = json.load(sys.stdin)
            verification = verify_with_arc(
                data,
                n_steps=args.steps,
                bins=args.bins,
                blend_mode=args.blend_mode
            )
            print(json.dumps(verification, indent=2))

            if args.visualize:
                visualize_integrity(
                    data,
                    n_steps=args.steps,
                    bins=args.bins,
                    blend_mode=args.blend_mode,
                    output_path=args.output,
                    render_mode=args.render_mode
                )
                if not args.output:
                    plt.show()
            return
        except json.JSONDecodeError as e:
            print(f"JSON error on stdin: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Fallback to common filenames
        candidates = [
            Path("/mnt/user-data/uploads/fibonacci_bloom_envelope.json"),
            Path("/mnt/data/fibonacci_bloom_envelope.json"),
            Path("fibonacci_bloom_envelope.json"),
            Path("correct_envelope.json"),
        ]
        path = next((p for p in candidates if p.exists()), None)
        if not path:
            parser.print_help()
            sys.exit(1)

    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        print(f"JSON error in {path}: {e}", file=sys.stderr)
        sys.exit(1)

    # Verify with Arc
    verification = verify_with_arc(
        data,
        n_steps=args.steps,
        bins=args.bins,
        blend_mode=args.blend_mode
    )
    print(json.dumps(verification, indent=2))

    # Visualize if requested
    if args.visualize:
        visualize_integrity(
            data,
            n_steps=args.steps,
            bins=args.bins,
            blend_mode=args.blend_mode,
            output_path=args.output,
            render_mode=args.render_mode
        )
        if not args.output:
            plt.show()


if __name__ == "__main__":
    main()
