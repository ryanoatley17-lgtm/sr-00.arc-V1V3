# sr-00.arc-V1V3

## Guardian-Arc × Fibonacci Bloom Integration

A unified cryptographic verification and geometric visualization system combining:
- **Fibonacci Bloom Integrity**: Cryptographic chain validation with golden ratio verification
- **Guardian-Arc vΩ**: Invariant density field visualization from pentagonal constellation dynamics

---

## Overview

This project integrates two mathematical systems that both leverage the golden ratio (φ):

### 1. Fibonacci Bloom Integrity Verifier
**File**: `full_verifier.py`

Validates Fibonacci-based cryptographic envelopes:
  1. **Eternal fingerprint** — SHA3-512 over serpent_bloom_core
  2. **Fibonacci coil chain** — Recursive fingerprint verification:
     - Coil 0: hash("0", "0", genesis, RESONANCE_HZ)
     - Coil 1: hash("0", fp_0, genesis, RESONANCE_HZ)
     - Coil n: hash(fp_(n-2), fp_(n-1), genesis, RESONANCE_HZ)
  3. **Phi ratio** — |phi_ratio_observed - φ| < PHI_TOL
  4. **External fingerprints** — Count, sources, algorithms

### 2. Guardian-Arc vΩ Density Field
**File**: `guardian_arc.py`

Generates invariant density fields using:
- **Pentagonal constellation** geometry (5 ring centers + 1 core)
- **Complex dynamics**: z → λ_φ(z - c) + c where λ_φ = exp(-1/φ + i·2π·φ)
- **Weighted sampling** from torch centers: [core, head, arm, foot, foot, arm]
- **Invariant density** ρ* visualization with logarithmic scaling

### 3. Arc Integrity Integration
**File**: `arc_integrity.py`

Bridges cryptography and geometry:
- **Fingerprint seeding**: Converts SHA3-512 hex fingerprints → trajectory seeds
- **Phi-weighted blending**: Combines multiple seeds using φ^(-i) weighting
- **Unified verification**: Numerical validation + visual density field analysis
- **Comparative visualization**: Side-by-side envelope integrity comparison

---

## Installation

### Requirements

```bash
pip install numpy matplotlib
```

### Files

- `full_verifier.py` — Fibonacci Bloom cryptographic verifier
- `guardian_arc.py` — Guardian-Arc density field generator
- `arc_integrity.py` — Integration module (verification + visualization)
- `example_arc_integration.py` — Demonstration examples

---

## Usage

### 1. Basic Fibonacci Verification

```bash
# Verify an envelope (JSON verification output)
python full_verifier.py envelope.json

# Or via stdin
cat envelope.json | python full_verifier.py
```

### 2. Guardian-Arc Visualization Only

```python
import guardian_arc
import matplotlib.pyplot as plt

# Generate trajectory
trajectory = guardian_arc.guardian_arc_trajectory(
    n_steps=2_000_000,
    burn_in=1_000,
    seed=0.123456789
)

# Compute density
density, x_edges, y_edges = guardian_arc.guardian_arc_density(
    trajectory, bins=512
)

# Plot
guardian_arc.guardian_arc_plot(density, x_edges, y_edges)
plt.savefig("arc_density.png", dpi=300)
```

### 3. Integrated Arc Integrity Verification

```bash
# Verify with Arc (JSON output)
python arc_integrity.py envelope.json

# Verify + visualize
python arc_integrity.py envelope.json --visualize --output arc_viz.png

# Advanced options
python arc_integrity.py envelope.json \
    --visualize \
    --steps 5000000 \
    --bins 768 \
    --blend-mode composite \
    --render-mode density \
    --output high_res_arc.png
```

### 4. Run Example Demonstrations

```bash
# Run all integration demos
python example_arc_integration.py

# Generates:
#   - arc_integrity_demo.png (single envelope visualization)
#   - arc_comparison_demo.png (3-envelope comparison)
```

---

## Integration Concepts

### Fingerprint-to-Seed Conversion

The integration maps cryptographic fingerprints to geometric seeds:

```python
# SHA3-512 hex string (128 chars)
fingerprint = "a3f2c9..."

# Extract first 64 bits → normalize to [0, 1)
seed = fingerprint_to_seed(fingerprint)  # → 0.641279...

# Generate trajectory seeded by fingerprint
trajectory = guardian_arc_trajectory(seed=seed)
```

### Phi-Weighted Seed Blending

Multiple Fibonacci coil fingerprints are combined using golden ratio weighting:

```python
seeds = [s₀, s₁, s₂, ..., sₙ]
weights = [φ⁰, φ⁻¹, φ⁻², ..., φ⁻ⁿ] / Σ

composite_seed = Σ(wᵢ · sᵢ)
```

This creates a unique geometric signature for each envelope's full coil chain.

### Visual Integrity Patterns

Valid vs invalid envelopes produce distinct density field patterns:
- **Valid envelope**: Stable pentagonal symmetry with clear torch centers
- **Corrupted envelope**: Distorted or asymmetric patterns
- **Different depths**: More coils → finer structure in density field

---

## API Reference

### `arc_integrity.py` Functions

#### `verify_with_arc(data, n_steps=2_000_000, bins=512, blend_mode="composite")`
Perform full verification with Guardian-Arc trajectory generation.

**Args:**
- `data`: Fibonacci Bloom Integrity Envelope (dict)
- `n_steps`: Trajectory steps (default: 2M)
- `bins`: Density grid resolution (default: 512)
- `blend_mode`: "composite" or "first" (default: "composite")

**Returns:** Verification report with `guardian_arc` metadata

---

#### `visualize_integrity(data, n_steps, bins, blend_mode, output_path, render_mode)`
Create integrated visualization showing verification summary + density field.

**Args:**
- `data`: Fibonacci Bloom Integrity Envelope
- `n_steps`: Trajectory steps
- `bins`: Density grid resolution
- `blend_mode`: "composite" or "first"
- `output_path`: Optional PNG save path
- `render_mode`: "density" or "hexbin"

**Returns:** `matplotlib.Figure`

---

#### `compare_envelopes(envelopes, labels, n_steps, bins, output_path)`
Compare multiple envelopes side-by-side with Guardian-Arc visualizations.

**Args:**
- `envelopes`: List of Fibonacci Bloom Integrity Envelopes
- `labels`: Optional labels for each envelope
- `n_steps`: Trajectory steps
- `bins`: Density grid resolution
- `output_path`: Optional PNG save path

**Returns:** `matplotlib.Figure`

---

#### `integrity_trajectory(bloom_core, n_steps, burn_in, blend_mode)`
Generate Guardian-Arc trajectory seeded by Fibonacci fingerprints.

**Args:**
- `bloom_core`: The `serpent_bloom_core` from envelope
- `n_steps`: Trajectory steps
- `burn_in`: Initial steps to discard
- `blend_mode`: "composite" or "first"

**Returns:** Complex numpy array trajectory

---

## Mathematical Background

### Golden Ratio (φ)

Both systems leverage φ = (1 + √5) / 2 ≈ 1.618033988749895:

- **Fibonacci Bloom**: Verifies phi_ratio in fingerprint chain
- **Guardian-Arc**: Uses λ_φ = exp(-1/φ + i·2π·φ) for complex dynamics

### Pentagonal Geometry

Guardian-Arc uses pentagonal (5-fold) symmetry:
- 5 ring centers at radius R = 3.5
- Angular positions: 0°, 72°, 144°, 216°, 288° (+ 90° offset)
- 1 core center at origin
- Total: 6 torch centers

### Invariant Density

The system converges to a unique invariant density ρ* satisfying:

```
ρ*(z) = Σᵢ wᵢ · ρ*(λ_φ⁻¹(z - cᵢ) + cᵢ)
```

where:
- wᵢ = weights for each torch center
- cᵢ = complex position of each torch center
- λ_φ = complex golden ratio operator

---

## Examples

### Example 1: Verify Valid Envelope

```bash
$ python arc_integrity.py envelope.json --visualize -o result.png

{
  "verification_result": "PASS",
  "eternal_fingerprint": {"ok": true, ...},
  "coil_chain": {"ok": true, "coils_checked": 13, ...},
  "phi_ratio": {"ok": true, "delta": 1.23e-10, ...},
  "guardian_arc": {
    "trajectory_steps": 1999000,
    "seeds_extracted": 13,
    "seed_used": 0.641279438262941
  }
}

Visualization saved to: result.png
```

### Example 2: Compare Envelopes Programmatically

```python
import json
from arc_integrity import compare_envelopes

# Load multiple envelopes
envelopes = [
    json.load(open("envelope_v1.json")),
    json.load(open("envelope_v2.json")),
    json.load(open("envelope_corrupted.json"))
]

# Generate comparison
fig = compare_envelopes(
    envelopes,
    labels=["Version 1", "Version 2", "Corrupted"],
    n_steps=1_000_000,
    bins=384,
    output_path="comparison.png"
)
```

### Example 3: Custom Trajectory Analysis

```python
from arc_integrity import integrity_trajectory, extract_fingerprint_seeds
import json

# Load envelope
envelope = json.load(open("envelope.json"))
bloom_core = envelope["serpent_bloom_core"]

# Extract seeds from coil chain
seeds = extract_fingerprint_seeds(bloom_core)
print(f"Extracted {len(seeds)} fingerprint seeds")

# Generate trajectory with composite blending
trajectory = integrity_trajectory(
    bloom_core,
    n_steps=5_000_000,
    burn_in=2_000,
    blend_mode="composite"
)

# Analyze trajectory properties
print(f"Trajectory bounds: {trajectory.real.min():.3f} to {trajectory.real.max():.3f}")
print(f"Mean position: {trajectory.mean()}")
```

---

## Performance Notes

### Trajectory Generation

- **Fast**: 500K steps ≈ 0.5 seconds
- **Standard**: 2M steps ≈ 2 seconds
- **High-quality**: 10M steps ≈ 10 seconds

### Density Estimation

- **Low-res**: 256 bins ≈ 0.1 seconds
- **Standard**: 512 bins ≈ 0.3 seconds
- **High-res**: 1024 bins ≈ 1.2 seconds

### Recommended Settings

| Use Case | Steps | Bins | Time |
|----------|-------|------|------|
| Quick preview | 500K | 256 | ~1s |
| Standard verification | 2M | 512 | ~3s |
| Publication quality | 10M | 1024 | ~15s |

---

## Design Philosophy

This integration demonstrates:

1. **Cryptographic-Geometric Duality**: Cryptographic fingerprints manifest as geometric patterns
2. **Phi-Coherence**: Both systems independently use φ, creating natural resonance
3. **Visual Verification**: Complex numerical validation becomes visually intuitive
4. **Fibonacci-Pentagonal Bridge**: Fibonacci sequences (1,1,2,3,5...) connect to pentagonal geometry (5-fold symmetry)

The Guardian-Arc density field acts as a "visual fingerprint" of the envelope's cryptographic integrity, where structural properties become geometric patterns.

---

## License

This project operates under a **dual licensing framework**:

1. **Mozilla Public License 2.0 (MPL-2.0)** — Code license, see [LICENSE](LICENSE)
2. **Grail Trust Custodial Addendum** — Symbolic framework license, see [GRAIL_TRUST_CUSTODIAL_ADDENDUM.md](GRAIL_TRUST_CUSTODIAL_ADDENDUM.md)

**See [LICENSE_NOTICE.md](LICENSE_NOTICE.md) for complete licensing guidance.**

### Summary

- **Code** (Python files): MPL-2.0 (permissive, file-level copyleft)
- **Symbolic frameworks** (ARC Bloom, Guardian-Arc mathematics): Grail Trust (custodial, non-exploitative)

The Grail Trust Custodial Addendum establishes:
- Custodial authorship by Ryan William Oatley
- Non-exploitation covenant (no weapons, surveillance, manipulation)
- Symbolic asset protection (no commoditization or tokenization)
- Integrity preservation requirements
- Succession and continuity framework

**All symbolic derivatives must comply with the Grail Trust Custodial Addendum.**

---

## Citation

If you use this work, please cite:

```
Guardian-Arc × Fibonacci Bloom Integration
sr-00.arc-V1V3
https://github.com/ryanoatley17-lgtm/sr-00.arc-V1V3
```

---

## Contributing

This is an integration demonstration project. For questions or contributions:
1. Open an issue describing your use case
2. Provide sample envelopes for testing
3. Include mathematical justification for proposed changes

---

**Status**: Fully integrated system with cryptographic verification and geometric visualization capabilities.
