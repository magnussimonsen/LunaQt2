"""Runtime style preference helpers."""

from __future__ import annotations

from dataclasses import dataclass, replace

from assets.fonts.font_lists import DEFAULT_UI_FONT
from .metrics import Metrics, build_metrics_for_ui_font


@dataclass(frozen=True)
class StylePreferences:
    """User-facing knobs that influence the generated QSS."""

    ui_font_family: str = DEFAULT_UI_FONT
    ui_font_size: int = Metrics().font_size_medium

    def build_metrics(self, template: Metrics | None = None) -> Metrics:
        """Return metrics adjusted to the current UI font settings."""

        metrics = build_metrics_for_ui_font(self.ui_font_size, template=template)
        return replace(metrics, font_family=self.ui_font_family)


__all__ = ["StylePreferences"]
