"""Matplotlib rcParams for theme-aware plot styling."""

from __future__ import annotations

# Light theme matplotlib configuration
MATPLOTLIB_LIGHT_STYLE: dict[str, str] = {
    # Figure and axes backgrounds
    "figure.facecolor": "#ffffff",
    "figure.edgecolor": "#ffffff",
    "axes.facecolor": "#ffffff",
    "axes.edgecolor": "#000000",
    
    # Grid
    "grid.color": "#d4d4d4",
    "grid.linestyle": "-",
    "grid.linewidth": "0.8",
    "grid.alpha": "0.5",
    
    # Text and labels
    "text.color": "#000000",
    "axes.labelcolor": "#000000",
    "axes.titlecolor": "#000000",
    "xtick.color": "#000000",
    "ytick.color": "#000000",
    "xtick.labelcolor": "#000000",
    "ytick.labelcolor": "#000000",
    
    # Spines
    "axes.spines.left": "True",
    "axes.spines.bottom": "True",
    "axes.spines.top": "False",
    "axes.spines.right": "False",
    
    # Lines and markers
    "lines.linewidth": "1.5",
    "lines.markersize": "6",
    
    # Legend
    "legend.facecolor": "#ffffff",
    "legend.edgecolor": "#d4d4d4",
    "legend.framealpha": "0.9",
    
    # Savefig
    "savefig.facecolor": "#ffffff",
    "savefig.edgecolor": "#ffffff",
    "savefig.dpi": "100",
}

# Dark theme matplotlib configuration
MATPLOTLIB_DARK_STYLE: dict[str, str] = {
    # Figure and axes backgrounds
    "figure.facecolor": "#1e1e1e",
    "figure.edgecolor": "#1e1e1e",
    "axes.facecolor": "#1e1e1e",
    "axes.edgecolor": "#f0f0f0",
    
    # Grid
    "grid.color": "#3c3c3c",
    "grid.linestyle": "-",
    "grid.linewidth": "0.8",
    "grid.alpha": "0.5",
    
    # Text and labels
    "text.color": "#f0f0f0",
    "axes.labelcolor": "#f0f0f0",
    "axes.titlecolor": "#f0f0f0",
    "xtick.color": "#f0f0f0",
    "ytick.color": "#f0f0f0",
    "xtick.labelcolor": "#f0f0f0",
    "ytick.labelcolor": "#f0f0f0",
    
    # Spines
    "axes.spines.left": "True",
    "axes.spines.bottom": "True",
    "axes.spines.top": "False",
    "axes.spines.right": "False",
    
    # Lines and markers
    "lines.linewidth": "1.5",
    "lines.markersize": "6",
    
    # Legend
    "legend.facecolor": "#1e1e1e",
    "legend.edgecolor": "#3c3c3c",
    "legend.framealpha": "0.9",
    
    # Savefig
    "savefig.facecolor": "#1e1e1e",
    "savefig.edgecolor": "#1e1e1e",
    "savefig.dpi": "100",
}


def get_matplotlib_style(is_dark_mode: bool) -> dict[str, str]:
    """Get matplotlib rcParams for the current theme mode.
    
    Args:
        is_dark_mode: Whether dark mode is active
        
    Returns:
        Dictionary of matplotlib rcParams
    """
    return dict(MATPLOTLIB_DARK_STYLE if is_dark_mode else MATPLOTLIB_LIGHT_STYLE)


__all__ = [
    "MATPLOTLIB_LIGHT_STYLE",
    "MATPLOTLIB_DARK_STYLE",
    "get_matplotlib_style",
]
