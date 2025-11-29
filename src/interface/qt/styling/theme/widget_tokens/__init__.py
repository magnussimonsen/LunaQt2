"""Per-widget spacing and border tokens derived from Metrics.

This package provides structured token classes for various UI widgets.
Each module contains a dataclass defining the spacing/border properties
and a factory function to construct it from Metrics.
"""

from .button_tokens import ButtonTokens, button_tokens
from .cell_container_tokens import CellContainerTokens, cell_container_tokens
from .cell_gutter_tokens import CellGutterTokens, cell_gutter_tokens
from .main_menubar_tokens import MenuBarTokens, menubar_tokens
from .main_toolbar_tokens import MainToolbarTokens, main_toolbar_tokens
from .sidebar_tokens import SidebarTokens, sidebar_tokens
from .statusbar_tokens import StatusBarTokens, statusbar_tokens

__all__ = [
    # Classes
    "ButtonTokens",
    "CellContainerTokens",
    "CellGutterTokens",
    "MenuBarTokens",
    "MainToolbarTokens",
    "SidebarTokens",
    "StatusBarTokens",
    # Factory functions
    "button_tokens",
    "cell_container_tokens",
    "cell_gutter_tokens",
    "menubar_tokens",
    "main_toolbar_tokens",
    "sidebar_tokens",
    "statusbar_tokens",
]
