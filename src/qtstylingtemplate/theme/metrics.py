"""Shared spacing and typography metrics used by all theme modules."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Metrics:
    """Spacing, sizing, and typography metrics shared by all styles."""

    radius_sm: int = 2
    radius_md: int = 4
    radius_lg: int = 6

    padding_xs: int = 2
    padding_sm: int = 4
    padding_md: int = 6
    padding_lg: int = 8

    gutter: int = 12
    toolbar_height: int = 32
    menubar_height: int = 28
    statusbar_height: int = 24

    font_family: str = "Segoe UI, 'Noto Sans', sans-serif"
    font_size_sm: int = 11
    font_size_md: int = 12
    font_size_lg: int = 14

    border_width: int = 1


__all__ = ["Metrics"]
