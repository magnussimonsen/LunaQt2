"""Central location for shared configuration constants."""

from .theme_startup_mode import DEFAULT_THEME_MODE
from .typography import (
	DEFAULT_UI_FONT_POINT_SIZE,
	FONT_SIZE_STEP,
	MAX_UI_FONT_POINT_SIZE,
	MIN_UI_FONT_POINT_SIZE,
	clamp_ui_font_point_size,
)
from assets.fonts.font_lists import BUNDLED_FONTS, DEFAULT_UI_FONT
from interface.qt.styling.theme.metrics import Metrics

_metrics = Metrics()
DEFAULT_SIDEBAR_WIDTH = _metrics.sidebar_default_width
MIN_SIDEBAR_WIDTH = _metrics.sidebar_min_width
MAX_SIDEBAR_WIDTH = _metrics.sidebar_max_width

__all__ = [
	"DEFAULT_THEME_MODE",
	"DEFAULT_SIDEBAR_WIDTH",
	"MIN_SIDEBAR_WIDTH",
	"MAX_SIDEBAR_WIDTH",
	"DEFAULT_UI_FONT_POINT_SIZE",
	"MIN_UI_FONT_POINT_SIZE",
	"MAX_UI_FONT_POINT_SIZE",
	"FONT_SIZE_STEP",
	"clamp_ui_font_point_size",
	"BUNDLED_FONTS",
	"DEFAULT_UI_FONT",
]
