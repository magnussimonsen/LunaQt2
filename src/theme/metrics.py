"""Shared spacing and typography metrics used by all theme modules."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Metrics:
    """Spacing, sizing, and typography metrics shared by all styles."""

    radius_small: int = 2
    radius_medium: int = 4
    radius_large: int = 6

    padding_extra_small: int = 2
    padding_small: int = 4
    padding_medium: int = 6
    padding_large: int = 8

    gutter: int = 12 # The width of cell gutter?
    toolbar_height: int = 32
    menubar_height: int = 28
    statusbar_height: int = 24

    font_family: str = "Segoe UI, 'Noto Sans', sans-serif"
    font_size_small: int = 11
    font_size_medium: int = 12
    font_size_large: int = 14

    border_width: int = 1


__all__ = ["Metrics"]
