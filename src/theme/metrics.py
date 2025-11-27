"""Shared spacing and typography metrics used by all theme modules."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Metrics:
    """Spacing, sizing, and typography metrics shared by all styles."""

    test_value: int = 80 # TESTING VALUE FOR DEBUGGING
   
    radius_zero: int = 0
    radius_small: int = 2
    radius_medium: int = 4
    radius_large: int = 6


    padding_zero: int = 0
    padding_extra_small: int = 2
    padding_small: int = 4
    padding_medium: int = 6
    padding_large: int = 8
    padding_extra_large: int = 12

    gutter_width: int = 12
    min_toolbar_height: int = 5
    min_menubar_height: int = 5
    min_statusbar_height: int = 32

    # Sidebar sizing
    sidebar_default_width: int = 320
    sidebar_min_width: int = 220
    sidebar_max_width: int = 560

    # FONT SIZE AND FAMILY WILL BE CONTROLLED BY A SEPERATE LOGIC, NOT HERE
    font_family: str = "Segoe UI, 'Noto Sans', sans-serif"
    font_size_small: int = 11
    font_size_medium: int = 12
    font_size_large: int = 14

    border_width: int = 1 # DEPRECATED
    border_width_zero: int = 0
    border_width_small: int = 1
    border_width_medium: int = 2
    border_width_large: int = 4


__all__ = ["Metrics"]
