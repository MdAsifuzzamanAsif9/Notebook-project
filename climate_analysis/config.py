"""Project-wide styling and display helpers."""

from __future__ import annotations

import matplotlib.pyplot as plt

DARK_BG = "#0d1117"
CARD_BG = "#161b22"
BORDER = "#30363d"
ACCENT1 = "#58a6ff"
ACCENT2 = "#3fb950"
ACCENT3 = "#ff7b72"
ACCENT4 = "#d2a8ff"
ACCENT5 = "#ffa657"
TEXT_PRI = "#e6edf3"
TEXT_SEC = "#8b949e"
PALETTE = [ACCENT1, ACCENT2, ACCENT3, ACCENT4, ACCENT5, "#f0e68c", "#20b2aa"]


def configure_theme() -> None:
    """Apply the shared Matplotlib theme used across charts."""
    plt.rcParams.update(
        {
            "figure.facecolor": DARK_BG,
            "axes.facecolor": CARD_BG,
            "axes.edgecolor": BORDER,
            "axes.labelcolor": TEXT_PRI,
            "xtick.color": TEXT_SEC,
            "ytick.color": TEXT_SEC,
            "text.color": TEXT_PRI,
            "grid.color": BORDER,
            "grid.linestyle": "--",
            "grid.alpha": 0.5,
            "font.family": "DejaVu Sans",
        }
    )


def print_section(title: str) -> None:
    """Print a section header for the command-line workflow."""
    line = "=" * len(title)
    print(f"\n{title}\n{line}")
