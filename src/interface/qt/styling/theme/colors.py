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
# Main application bg colors (not cells and cell gutters)
app_bg_light = "#dddddd"
app_bg_dark = "#1e1e1e"

main_menubar_bg_light = "#aaaaaa"
main_menubar_bg_dark = "#2c2c2c"

main_toolbar_bg_light = "#aaaaaa"
main_toolbar_bg_dark = "#2c2c2c"

main_dropdown_bg_light = "#dddddd"
main_dropdown_bg_dark = "#333333"

sidebar_header_bg_light = "#aaaaaa"
sidebar_header_bg_dark = "#2c2c2c"

sidebar_toolbar_bg_light = "#aaaaaa"
sidebar_toolbar_bg_dark = "#2c2c2c"

sidebar_content_bg_light = "#aaaaaa"
sidebar_content_bg_dark = "#2c2c2c"

cell_bg_light = "#dddddd"
cell_bg_dark = "#2c2c2c"

cell_selected_bg_light = "#e6e6e6"
cell_selected_bg_dark = "#2a2a2a"

cell_gutter_bg_light = "#cccccc"
cell_gutter_bg_dark = "#2c2c2c"

# Button colors
button_bg_light = "#f0f0f0"
button_bg_dark = "#3a3a3a"

# Hover/Selected/pressed item colors
hover_item_bg_light = "#a3c4e0" # OBS: Do not change bg on hover for cells (border only)
hover_item_bg_dark = "#4a4a4a" # OBS: Do not change bg on hover for cells (border only)

hover_item_border_light = "#a3c4e0"
hover_item_border_dark = "#4a4a4a" 

item_pressed_bg_light = "#6da9d9"  # OBS: Do not change bg on pressed for cells (border only)
item_pressed_bg_dark = "#232323"   # OBS: Do not change bg on pressed for cells (border only)

item_pressed_border_light = "#6da9d9"
item_pressed_border_dark = "#6da9d9"

selected_item_bg_light = "#3294d6" # OBS: Do not change bg on selected for cells (border only)
selected_item_bg_dark = "#264DE4" # OBS: Do not change bg on selected for cells (border only)

selected_item_border_light = "#3294d6"
selected_item_border_dark = "#264DE4"

# Cell- and gutter-specific border and bg colors (cells don't change background on hover/pressed/selected, but gutters do cnahge bg on selected)
cell_bg_light = "#dddddd"
cell_bg_dark = "#2c2c2c"

cell_gutter_bg_light = "#cccccc"
cell_gutter_bg_dark = "#2c2c2c"

hover_cell_border_light = "#a3c4e0"
hover_cell_border_dark = "#4a4a4a" 

hover_gutter_border_light = "#a3c4e0"
hover_gutter_border_dark = "#4a4a4a" 

cell_pressed_border_light = "#6da9d9"
cell_pressed_border_dark = "#6da9d9"

gutter_pressed_border_light = "#6da9d9"
gutter_pressed_border_dark = "#6da9d9"

cell_selected_bg_light = cell_bg_light
cell_selected_bg_dark = cell_bg_dark

selected_cell_border_light = "#3294d6"
selected_cell_border_dark = "#264DE4"

selected_gutter_border_light = "#3294d6"
selected_gutter_border_dark = "#264DE4"

selected_gutter_bg_light = "#3294d6"  # OBS: Gutter changes bg on selected
selected_gutter_bg_dark = "#264DE4"   # OBS: Gutter changes bg on selected

# General UI border colors
subtle_border_light = "#343434"
subtle_border_dark = "#2B2B2B"

normal_border_light = "#ffcccc"
normal_border_dark = "#663333"

button_border_light = "#bcbcbc"
button_border_dark = "#707070"

class _BGTokens:
    app_bg = ModeAwareColor(light=app_bg_light, dark=app_bg_dark)
    menubar_bg = ModeAwareColor(light=main_menubar_bg_light, dark=main_menubar_bg_dark)
    dropdown_bg = ModeAwareColor(light=main_dropdown_bg_light, dark=main_dropdown_bg_dark)
    statusbar_bg = ModeAwareColor(light=main_menubar_bg_light, dark=main_menubar_bg_dark)
    toolbar_bg = ModeAwareColor(light=main_toolbar_bg_light, dark=main_toolbar_bg_dark)
    sidebar_bg = ModeAwareColor(light=sidebar_content_bg_light, dark=sidebar_content_bg_dark)
    
    cell_bg = ModeAwareColor(light=cell_bg_light, dark=cell_bg_dark)
    cell_selected_bg = ModeAwareColor(light=cell_selected_bg_light, dark=cell_selected_bg_dark)
    cell_gutter_bg = ModeAwareColor(light=cell_gutter_bg_light, dark=cell_gutter_bg_dark)
    selected_gutter_bg = ModeAwareColor(light=selected_gutter_bg_light, dark=selected_gutter_bg_dark)
   
    sidebar_header_bg = ModeAwareColor(light=sidebar_header_bg_light, dark=sidebar_header_bg_dark)
    sidebar_toolbar_bg = ModeAwareColor(light=sidebar_toolbar_bg_light, dark=sidebar_toolbar_bg_dark)
    sidebar_content_bg = ModeAwareColor(light=sidebar_content_bg_light, dark=sidebar_content_bg_dark)
    hover_bg = ModeAwareColor(light=hover_item_bg_light, dark=hover_item_bg_dark)


class _BorderTokens:
    transparent_border = ModeAwareColor(light=app_bg_light, dark=app_bg_dark)
    subtle_border = ModeAwareColor(light=subtle_border_light, dark=subtle_border_dark)
    normal_border = ModeAwareColor(light=normal_border_light, dark=normal_border_dark)
    hover_border = ModeAwareColor(light=hover_item_border_light, dark=hover_item_border_dark)
    pressed_border = ModeAwareColor(light=item_pressed_border_light, dark=item_pressed_border_dark)
    selected_border = ModeAwareColor(light=selected_item_border_light, dark=selected_item_border_dark)
    cell_border = ModeAwareColor(light=subtle_border_light, dark=subtle_border_dark)
    cell_hover_border = ModeAwareColor(light=hover_cell_border_light, dark=hover_cell_border_dark)
    cell_pressed_border = ModeAwareColor(light=cell_pressed_border_light, dark=cell_pressed_border_dark)
    cell_in_focus_border = ModeAwareColor(light=selected_cell_border_light, dark=selected_cell_border_dark)
    cell_gutter_border = ModeAwareColor(light="#d5d5d5", dark="#2a2a2a")
    gutter_hover_border = ModeAwareColor(light=hover_gutter_border_light, dark=hover_gutter_border_dark)
    gutter_pressed_border = ModeAwareColor(light=gutter_pressed_border_light, dark=gutter_pressed_border_dark)
    gutter_in_focus_border = ModeAwareColor(light=selected_gutter_border_light, dark=selected_gutter_border_dark)


class _TextTokens:
    primary = ModeAwareColor(light="#111111", dark="#fafafa")
    secondary = ModeAwareColor(light="#333333", dark="#c0c0c0")
    muted = ModeAwareColor(light="#666666", dark="#8a8a8a")
    warning = ModeAwareColor(light="#b05a00", dark="#f5d17a")


class _ViewportTokens:
    base = _BGTokens.cell_bg
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
        hover=ModeAwareColor(light=hover_item_bg_light, dark=hover_item_bg_dark),
        pressed=ModeAwareColor(light="#c0c0c0", dark="#303030"),
        disabled=ModeAwareColor(light="#f0f0f0", dark="#292929"),
        border=ModeAwareColor(light=button_border_light, dark=button_border_dark),
        text=_TextTokens.primary,
        focus=_BorderTokens.selected_border,
    )
    main_toolbar = ButtonPaletteTokens( 
        normal=ModeAwareColor(light=button_bg_light, dark=button_bg_dark),
        hover=ModeAwareColor(light=hover_item_bg_light, dark=hover_item_bg_dark),
        pressed=ModeAwareColor(light=item_pressed_bg_light, dark=item_pressed_bg_dark),
        disabled=ModeAwareColor(light="#f8f8f8", dark="#1a1a1a"),
        border=ModeAwareColor(light="#dadada", dark="#404040"),
        text=_TextTokens.secondary,
        focus=_BorderTokens.selected_border,
    )

    sidebar_toolbar = ButtonPaletteTokens( 
        normal=ModeAwareColor(light=button_bg_light, dark=button_bg_dark),
        hover=ModeAwareColor(light=hover_item_bg_light, dark=hover_item_bg_dark),
        pressed=ModeAwareColor(light=item_pressed_bg_light, dark=item_pressed_bg_dark),
        disabled=ModeAwareColor(light="#f8f8f8", dark="#1a1a1a"),
        border=ModeAwareColor(light="#dadada", dark="#404040"),
        text=_TextTokens.secondary,
        focus=_BorderTokens.selected_border,
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
        normal=ModeAwareColor(light=button_bg_light, dark=button_bg_dark),
        hover=ModeAwareColor(light=hover_item_bg_light, dark=hover_item_bg_dark),
        pressed=ModeAwareColor(light=selected_item_bg_light, dark=selected_item_bg_dark),
        disabled=ModeAwareColor(light="#f8f8f8", dark="#1f1f1f"),
        border=ModeAwareColor(light=button_border_light, dark="#5a5a5a"),
        text=_TextTokens.primary,
        focus=_BorderTokens.selected_border,
    )


class _MenuTokens:
    background = _BGTokens.menubar_bg
    text = _TextTokens.primary
    item_hover = ModeAwareColor(light=hover_item_bg_light, dark=hover_item_bg_dark)
    separator = _BorderTokens.subtle_border


class _StatusBarTokens:
    background = _BGTokens.statusbar_bg
    text = _TextTokens.secondary
    border_top = _BorderTokens.subtle_border
    warning = _TextTokens.warning


@dataclass(frozen=True)
class BackgroundPalette:
    app: str
    menubar: str
    statusbar: str
    dropdown: str
    cell: str
    cell_selected: str
    cell_gutter: str
    selected_gutter: str
    toolbar: str
    sidebar_bg: str
    sidebar_header: str
    sidebar_toolbar: str
    sidebar_content: str
    hover: str


@dataclass(frozen=True)
class BorderPalette:
    transparent: str
    subtle: str
    strong: str
    hover: str
    pressed: str
    selected: str
    cell: str
    cell_hover: str
    cell_pressed: str
    cell_in_focus: str
    cell_gutter: str
    gutter_hover: str
    gutter_pressed: str
    gutter_in_focus: str


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
        app=tokens.app_bg.value_for(mode),
        menubar=tokens.menubar_bg.value_for(mode),
        statusbar=tokens.statusbar_bg.value_for(mode),
        dropdown=tokens.dropdown_bg.value_for(mode),
        cell=tokens.cell_bg.value_for(mode),
        cell_selected=tokens.cell_selected_bg.value_for(mode),
        cell_gutter=tokens.cell_gutter_bg.value_for(mode),
        selected_gutter=tokens.selected_gutter_bg.value_for(mode),
        toolbar=tokens.toolbar_bg.value_for(mode),
        sidebar_bg=tokens.sidebar_bg.value_for(mode),
        sidebar_header=tokens.sidebar_header_bg.value_for(mode),
        sidebar_content=tokens.sidebar_content_bg.value_for(mode),
        sidebar_toolbar=tokens.sidebar_toolbar_bg.value_for(mode),
        hover=tokens.hover_bg.value_for(mode),
    )


def _resolve_border(mode: ThemeMode) -> BorderPalette:
    tokens = _BorderTokens
    return BorderPalette(
        transparent=tokens.transparent_border.value_for(mode),
        subtle=tokens.subtle_border.value_for(mode),
        strong=tokens.normal_border.value_for(mode),
        hover=tokens.hover_border.value_for(mode),
        pressed=tokens.pressed_border.value_for(mode),
        selected=tokens.selected_border.value_for(mode),
        cell=tokens.cell_border.value_for(mode),
        cell_hover=tokens.cell_hover_border.value_for(mode),
        cell_pressed=tokens.cell_pressed_border.value_for(mode),
        cell_in_focus=tokens.cell_in_focus_border.value_for(mode),
        cell_gutter=tokens.cell_gutter_border.value_for(mode),
        gutter_hover=tokens.gutter_hover_border.value_for(mode),
        gutter_pressed=tokens.gutter_pressed_border.value_for(mode),
        gutter_in_focus=tokens.gutter_in_focus_border.value_for(mode),
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
