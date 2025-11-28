"""Centralized color palette and spacing metrics for the application."""

from __future__ import annotations

from dataclasses import dataclass

from .metrics import Metrics
from .mode import ThemeMode


@dataclass(frozen=True)
class ModeAwareColor:
    """Represents a color that supports both light and dark variants."""

    light: str
    dark: str

    def value_for(self, mode: ThemeMode) -> str:
        return self.light if mode == ThemeMode.LIGHT else self.dark

    def __str__(self) -> str:  # pragma: no cover - convenience for debugging
        return self.dark

# Define base color palettes
l1 = "#dddddd"  # Main app bg - Light mode
d1 = "#1e1e1e"  # Main app bg - Dark mode
l2 = "#aaaaaa"  # Menu bar and status bar bg
d2 = "#2c2c2c"
l3 = "#aaaaaa"  # Toolbar bg
d3 = "#e2e2e2"
l4 = "#dddddd"  # Dropdown bg
d4 = "#333333"
l5 = "#70b3ff"  # Hover bg (blueish)
d5 = "#232323"
l6 = "#f0f0f0"  # Button bg color
d6 = "#3a3a3a"
l7 = "#3352FF"  # Selected items bg /Highlight
d7 = "#264DE4"
l8 = "#cccccc"  # Cell gutter bg
d8 = "#181818"
l9 = "#dddddd"  # Cell bg 
d9 = "#b5b5b5"
l10 = "#343434"  # Border color subtle light mode
d10 = "#2B2B2B"  # Border color subtle dark mode
l11 = "#ffcccc"  # Border color normal strong light mode
d11 = "#663333"  # Border color normal strong dark mode

class _BGTokens:
    app = ModeAwareColor(light=l1, dark=d1)
    menubar = ModeAwareColor(light=l2, dark=d2)
    statusbar = ModeAwareColor(light=l2, dark=d2)
    toolbar = ModeAwareColor(light=l3, dark=d3) # Same for main and sidebar toolbars for consistency
    dropdown = ModeAwareColor(light=l4, dark=d4)
    cell = ModeAwareColor(light=l9, dark=d9)
    cell_gutter = ModeAwareColor(light=l8, dark=d8)
    sidebar_header = ModeAwareColor(light="#C266FF", dark="#2a2a2a")
    sidebar_content = ModeAwareColor(light="#F5FF66", dark="#2a2a2a")
    sidebar_toolbar = ModeAwareColor(light="#A70707", dark="#333333")


class _BorderTokens:
    transparent = ModeAwareColor(light=l1, dark=d1)
    subtle = ModeAwareColor(light=l10, dark=d10)
    strong = ModeAwareColor(light=l11, dark=d11)
    highlight = ModeAwareColor(light=l7, dark=d7)
    cell = ModeAwareColor(light=l10, dark=d10)
    cell_gutter = ModeAwareColor(light="#d5d5d5", dark="#2a2a2a")
    cell_in_focus = ModeAwareColor(light="#ff0000", dark="#5ea2ff")


class _TextTokens:
    primary = ModeAwareColor(light="#111111", dark="#fafafa")
    secondary = ModeAwareColor(light="#333333", dark="#c0c0c0")
    muted = ModeAwareColor(light="#666666", dark="#8a8a8a")
    warning = ModeAwareColor(light="#b05a00", dark="#f5d17a")


class _ViewportTokens:
    base = _BGTokens.cell
    alternate = ModeAwareColor(light="#f6f6f6", dark="#232323")
    selection = ModeAwareColor(light="#cfe1ff", dark="#2e4a70")
    selection_text = _TextTokens.primary


@dataclass(frozen=True)
class ButtonPaletteTokens:
    normal: ModeAwareColor
    hover: ModeAwareColor
    pressed: ModeAwareColor
    disabled: ModeAwareColor
    border: ModeAwareColor
    text: ModeAwareColor
    focus: ModeAwareColor

    def resolve(self, mode: ThemeMode) -> "ButtonPalette":
        return ButtonPalette(
            normal=self.normal.value_for(mode),
            hover=self.hover.value_for(mode),
            pressed=self.pressed.value_for(mode),
            disabled=self.disabled.value_for(mode),
            border=self.border.value_for(mode),
            text=self.text.value_for(mode),
            focus=self.focus.value_for(mode),
        )


class _ButtonTokens:
    primary = ButtonPaletteTokens(
        normal=ModeAwareColor(light="#e0e0e0", dark="#404040"),
        hover=ModeAwareColor(light=l5, dark=d5),
        pressed=ModeAwareColor(light="#c0c0c0", dark="#303030"),
        disabled=ModeAwareColor(light="#f0f0f0", dark="#292929"),
        border=ModeAwareColor(light="#bcbcbc", dark="#707070"),
        text=_TextTokens.primary,
        focus=_BorderTokens.highlight,
    )
    main_toolbar = ButtonPaletteTokens( 
        normal=ModeAwareColor(light=l6, dark=d6),
        hover=ModeAwareColor(light=l5, dark=d5),
        pressed=ModeAwareColor(light="#dcdcdc", dark="#1f1f1f"),
        disabled=ModeAwareColor(light="#f8f8f8", dark="#1a1a1a"),
        border=ModeAwareColor(light="#dadada", dark="#404040"),
        text=_TextTokens.secondary,
        focus=_BorderTokens.highlight,
    )

    sidebar_toolbar = ButtonPaletteTokens( 
        normal=ModeAwareColor(light=l6, dark=d6),
        hover=ModeAwareColor(light=l5, dark=d5),
        pressed=ModeAwareColor(light="#dcdcdc", dark="#1f1f1f"),
        disabled=ModeAwareColor(light="#f8f8f8", dark="#1a1a1a"),
        border=ModeAwareColor(light="#dadada", dark="#404040"),
        text=_TextTokens.secondary,
        focus=_BorderTokens.highlight,
    )

    warning = ButtonPaletteTokens(
        normal=ModeAwareColor(light="#fbe2c5", dark="#6a381f"),
        hover=ModeAwareColor(light="#f8d4a3", dark="#7c4225"),
        pressed=ModeAwareColor(light="#f4c07e", dark="#4d2817"),
        disabled=ModeAwareColor(light="#fdf0df", dark="#3a1c10"),
        border=ModeAwareColor(light="#f2a25d", dark="#c4672e"),
        text=_TextTokens.primary,
        focus=ModeAwareColor(light="#ff8800", dark="#ffa45c"),
    )
    menubar = ButtonPaletteTokens(
        normal=ModeAwareColor(light=l6, dark=d6),
        hover=ModeAwareColor(light=l5, dark=d5),
        pressed=ModeAwareColor(light="#4a90e2", dark="#5a9fff"),
        disabled=ModeAwareColor(light="#f8f8f8", dark="#1f1f1f"),
        border=ModeAwareColor(light="#bcbcbc", dark="#5a5a5a"),
        text=_TextTokens.primary,
        focus=_BorderTokens.highlight,
    )


class _MenuTokens:
    background = _BGTokens.menubar
    text = _TextTokens.primary
    item_hover = ModeAwareColor(light=l5, dark=d5)
    separator = _BorderTokens.subtle


class _StatusBarTokens:
    background = _BGTokens.statusbar
    text = _TextTokens.secondary
    border_top = _BorderTokens.subtle
    warning = _TextTokens.warning


@dataclass(frozen=True)
class BackgroundPalette:
    app: str
    menubar: str
    statusbar: str
    dropdown: str
    cell: str
    cell_gutter: str
    toolbar: str
    sidebar_header: str
    sidebar_toolbar: str
    sidebar_content: str


@dataclass(frozen=True)
class BorderPalette:
    transparent: str
    subtle: str
    strong: str
    highlight: str
    cell: str
    cell_gutter: str
    cell_in_focus: str


@dataclass(frozen=True)
class TextPalette:
    primary: str
    secondary: str
    muted: str
    warning: str


@dataclass(frozen=True)
class ViewportPalette:
    base: str
    alternate: str
    selection: str
    selection_text: str


@dataclass(frozen=True)
class ButtonPalette:
    normal: str
    hover: str
    pressed: str
    disabled: str
    border: str
    text: str
    focus: str


@dataclass(frozen=True)
class ButtonPalettes:
    primary: ButtonPalette
    main_toolbar: ButtonPalette
    sidebar_toolbar: ButtonPalette
    menubar: ButtonPalette
    warning: ButtonPalette


@dataclass(frozen=True)
class MenuPalette:
    background: str
    text: str
    item_hover: str
    separator: str


@dataclass(frozen=True)
class StatusBarPalette:
    background: str
    text: str
    border_top: str
    warning: str


@dataclass(frozen=True)
class Theme:
    mode: ThemeMode
    bg: BackgroundPalette
    border: BorderPalette
    text: TextPalette
    viewport: ViewportPalette
    buttons: ButtonPalettes
    menu: MenuPalette
    statusbar: StatusBarPalette
    metrics: Metrics


def _resolve_bg(mode: ThemeMode) -> BackgroundPalette:
    tokens = _BGTokens
    return BackgroundPalette(
        app=tokens.app.value_for(mode),
        menubar=tokens.menubar.value_for(mode),
        statusbar=tokens.statusbar.value_for(mode),
        dropdown=tokens.dropdown.value_for(mode),
        cell=tokens.cell.value_for(mode),
        cell_gutter=tokens.cell_gutter.value_for(mode),
        toolbar=tokens.toolbar.value_for(mode),
        sidebar_header=tokens.sidebar_header.value_for(mode),
        sidebar_content=tokens.sidebar_content.value_for(mode),
        sidebar_toolbar=tokens.sidebar_toolbar.value_for(mode),
    )


def _resolve_border(mode: ThemeMode) -> BorderPalette:
    tokens = _BorderTokens
    return BorderPalette(
        transparent=tokens.transparent.value_for(mode),
        subtle=tokens.subtle.value_for(mode),
        strong=tokens.strong.value_for(mode),
        highlight=tokens.highlight.value_for(mode),
        cell=tokens.cell.value_for(mode),
        cell_gutter=tokens.cell_gutter.value_for(mode),
        cell_in_focus=tokens.cell_in_focus.value_for(mode),
    )


def _resolve_text(mode: ThemeMode) -> TextPalette:
    tokens = _TextTokens
    return TextPalette(
        primary=tokens.primary.value_for(mode),
        secondary=tokens.secondary.value_for(mode),
        muted=tokens.muted.value_for(mode),
        warning=tokens.warning.value_for(mode),
    )


def _resolve_viewport(mode: ThemeMode) -> ViewportPalette:
    tokens = _ViewportTokens
    return ViewportPalette(
        base=tokens.base.value_for(mode),
        alternate=tokens.alternate.value_for(mode),
        selection=tokens.selection.value_for(mode),
        selection_text=tokens.selection_text.value_for(mode),
    )


def _resolve_buttons(mode: ThemeMode) -> ButtonPalettes:
    tokens = _ButtonTokens
    return ButtonPalettes(
        primary=tokens.primary.resolve(mode),
        main_toolbar=tokens.main_toolbar.resolve(mode),
        sidebar_toolbar=tokens.sidebar_toolbar.resolve(mode),
        menubar=tokens.menubar.resolve(mode),
        warning=tokens.warning.resolve(mode),
    )


def _resolve_menu(mode: ThemeMode) -> MenuPalette:
    tokens = _MenuTokens
    return MenuPalette(
        background=tokens.background.value_for(mode),
        text=tokens.text.value_for(mode),
        item_hover=tokens.item_hover.value_for(mode),
        separator=tokens.separator.value_for(mode),
    )


def _resolve_statusbar(mode: ThemeMode) -> StatusBarPalette:
    tokens = _StatusBarTokens
    return StatusBarPalette(
        background=tokens.background.value_for(mode),
        text=tokens.text.value_for(mode),
        border_top=tokens.border_top.value_for(mode),
        warning=tokens.warning.value_for(mode),
    )


def get_theme(mode: ThemeMode = ThemeMode.DARK, metrics: Metrics | None = None) -> Theme:
    """Return a fully resolved palette for the requested theme mode."""

    metrics = metrics or Metrics()
    return Theme(
        mode=mode,
        bg=_resolve_bg(mode),
        border=_resolve_border(mode),
        text=_resolve_text(mode),
        viewport=_resolve_viewport(mode),
        buttons=_resolve_buttons(mode),
        menu=_resolve_menu(mode),
        statusbar=_resolve_statusbar(mode),
        metrics=metrics,
    )


__all__ = [
    "ThemeMode",
    "ModeAwareColor",
    "Metrics",
    "Theme",
    "ButtonPalette",
    "ButtonPalettes",
    "BackgroundPalette",
    "BorderPalette",
    "TextPalette",
    "ViewportPalette",
    "MenuPalette",
    "StatusBarPalette",
    "get_theme",
]
