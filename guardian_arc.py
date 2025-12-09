"""
Guardian-Arc vΩ: invariant density field.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

# Canonical constants
phi = (1 + np.sqrt(5)) / 2
lambda_phi = np.exp(-1 / phi + 1j * 2 * np.pi * phi)

# Pentagonal constellation
R_CONSTELLATION = 3.5
_angles = np.linspace(0, 2 * np.pi, 5, endpoint=False) + np.pi / 2
_ring_centers = R_CONSTELLATION * np.exp(1j * _angles)
CENTERS = np.concatenate(([0.0 + 0.0j], _ring_centers))  # 0 = core

# Torch weights: [core, head, arm, foot, foot, arm]
W_CORE = 0.30
W_HEAD = 0.25
W_ARM = 0.15
W_FOOT = 0.075

WEIGHTS = np.array(
    [W_CORE, W_HEAD, W_ARM, W_FOOT, W_FOOT, W_ARM], dtype=float
)
WEIGHTS /= WEIGHTS.sum()
CUTS = np.cumsum(WEIGHTS)


def guardian_arc_trajectory(
    n_steps: int = 2_000_000,
    burn_in: int = 1_000,
    seed: float = 0.123456789,
) -> np.ndarray:
    """
    Generate complex trajectory samples approximating the invariant density ρ*.
    """
    s = float(seed) % 1.0
    z = 0.0 + 0.0j
    traj = np.zeros(n_steps, dtype=complex)

    for i in range(n_steps):
        s = (s + phi) % 1.0
        k = np.searchsorted(CUTS, s)
        c = CENTERS[k]
        z = lambda_phi * (z - c) + c
        traj[i] = z

    if burn_in > 0:
        traj = traj[burn_in:]
    return traj


def guardian_arc_density(
    z: np.ndarray,
    bins: int = 512,
    extent: tuple | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Estimate 2D density on a regular grid from complex samples z.
    """
    x = z.real
    y = z.imag

    if extent is None:
        xmin, xmax = x.min(), x.max()
        ymin, ymax = y.min(), y.max()
        dx = xmax - xmin
        dy = ymax - ymin
        margin = 0.05
        xmin -= margin * dx
        xmax += margin * dx
        ymin -= margin * dy
        ymax += margin * dy
        extent = (xmin, xmax, ymin, ymax)

    xmin, xmax, ymin, ymax = extent
    H, x_edges, y_edges = np.histogram2d(
        x, y, bins=bins, range=[[xmin, xmax], [ymin, ymax]]
    )
    # transpose for standard image orientation
    return H.T, x_edges, y_edges


def guardian_arc_plot(
    density: np.ndarray,
    x_edges: np.ndarray,
    y_edges: np.ndarray,
    ax: plt.Axes | None = None,
    cmap: str = "inferno",
):
    """
    Plot the invariant field density ρ* with logarithmic scaling.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 10))
    else:
        fig = ax.figure

    # Avoid log(0) issues
    data = density.copy()
    data[data <= 0] = np.nan
    norm = LogNorm(vmin=np.nanmin(data), vmax=np.nanmax(data))

    X, Y = np.meshgrid(x_edges, y_edges)
    im = ax.pcolormesh(X, Y, density, norm=norm, cmap=cmap, shading="auto")

    ax.scatter(
        CENTERS.real,
        CENTERS.imag,
        c="white",
        s=20,
        alpha=0.6,
        marker="+",
    )

    ax.set_aspect("equal")
    ax.set_axis_off()
    ax.set_title("GUARDIAN-ARC vΩ\nInvariant Density ρ*")

    cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cb.set_label("Field Probability Density (Log Scale)")

    return ax, im, cb


def guardian_arc_hexbin(
    z: np.ndarray,
    gridsize: int = 400,
    ax: plt.Axes | None = None,
    cmap: str = "inferno",
):
    """
    Alternative hexbin rendering of ρ* directly from samples.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 10))
    else:
        fig = ax.figure

    x = z.real
    y = z.imag

    hb = ax.hexbin(
        x,
        y,
        gridsize=gridsize,
        cmap=cmap,
        norm=LogNorm(),
        linewidths=0,
    )

    ax.scatter(
        CENTERS.real,
        CENTERS.imag,
        c="white",
        s=20,
        alpha=0.6,
        marker="+",
    )

    ax.set_aspect("equal")
    ax.set_axis_off()
    ax.set_title("GUARDIAN-ARC vΩ\nInvariant Density ρ*")

    cb = fig.colorbar(hb, ax=ax, fraction=0.046, pad=0.04)
    cb.set_label("Field Probability Density (Log Scale)")

    return ax, hb, cb


__all__ = [
    "CENTERS",
    "WEIGHTS",
    "CUTS",
    "guardian_arc_trajectory",
    "guardian_arc_density",
    "guardian_arc_plot",
    "guardian_arc_hexbin",
]
