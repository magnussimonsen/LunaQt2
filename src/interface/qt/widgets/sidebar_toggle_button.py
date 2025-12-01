"""Reusable menubar button that toggles a sidebar dock."""

from __future__ import annotations

from collections.abc import Callable

from PySide6.QtWidgets import QPushButton, QWidget


class SidebarToggleButton(QPushButton):
    """Checkable button that calls back when toggled and refreshes its style."""

    def __init__(
        self,
        label: str,
        on_toggle: Callable[[bool], None],
        *,
        parent: QWidget | None = None,
        btn_type: str = "menubar",
        tooltip: str | None = None,
    ) -> None:
        super().__init__(label, parent)
        self._on_toggle = on_toggle

        self.setCheckable(True)
        self.setProperty("btnType", btn_type)
        if tooltip:
            self.setToolTip(tooltip)

        self.toggled.connect(self._handle_toggled)

    def _handle_toggled(self, checked: bool) -> None:
        self._on_toggle(checked)
        self.refresh_style()

    def refresh_style(self) -> None:
        """Reapply the style so QSS rules respond to state changes."""

        style = self.style()
        style.unpolish(self)
        style.polish(self)
        self.update()


__all__ = ["SidebarToggleButton"]
