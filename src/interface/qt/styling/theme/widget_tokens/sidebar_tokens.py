"""Sidebar spacing and border tokens derived from Metrics."""

from __future__ import annotations

from dataclasses import dataclass

from ..metrics import Metrics


@dataclass(frozen=True)
class SidebarTokens:
    # Sidebar container tokens
    sidebar_container_border_radius: int
    sidebar_container_border_width_top: int
    sidebar_container_border_width_bottom: int
    sidebar_container_border_width_left: int
    sidebar_container_border_width_right: int

    # Sidebar header tokens
    sidebar_header_border_top_width: int
    sidebar_header_border_bottom_width: int
    sidebar_header_border_left_width: int
    sidebar_header_border_right_width: int
    sidebar_header_padding_top: int
    sidebar_header_padding_bottom: int
    sidebar_header_padding_left: int
    sidebar_header_padding_right: int
    sidebar_header_margin_top: int
    sidebar_header_margin_bottom: int
    sidebar_header_margin_left: int
    sidebar_header_margin_right: int

    # Sidebar toolbar tokens
    sidebar_toolbar_border_radius: int
    sidebar_toolbar_border_top_width: int
    sidebar_toolbar_border_bottom_width: int
    sidebar_toolbar_border_left_width: int
    sidebar_toolbar_border_right_width: int
    sidebar_toolbar_padding_top: int
    sidebar_toolbar_padding_bottom: int
    sidebar_toolbar_padding_left: int
    sidebar_toolbar_padding_right: int
    sidebar_toolbar_margin_top: int
    sidebar_toolbar_margin_bottom: int
    sidebar_toolbar_margin_left: int
    sidebar_toolbar_margin_right: int
    sidebar_toolbar_item_x_spacing: int
    sidebar_toolbar_item_padding_top: int
    sidebar_toolbar_item_padding_bottom: int
    sidebar_toolbar_item_padding_left: int
    sidebar_toolbar_item_padding_right: int

    # Sidebar content container tokens
    sidebar_content_border_radius: int
    sidebar_content_border_top_width: int
    sidebar_content_border_bottom_width: int
    sidebar_content_border_left_width: int
    sidebar_content_border_right_width: int
    sidebar_content_margin_top: int
    sidebar_content_margin_bottom: int
    sidebar_content_margin_left: int
    sidebar_content_margin_right: int

    # Sidebar content item tokens
    sidebar_content_item_border_top_width: int
    sidebar_content_item_border_bottom_width: int
    sidebar_content_item_border_left_width: int
    sidebar_content_item_border_right_width: int
    sidebar_content_item_x_spacing: int
    sidebar_content_item_padding_top: int
    sidebar_content_item_padding_bottom: int
    sidebar_content_item_padding_left: int
    sidebar_content_item_padding_right: int
    sidebar_content_item_margin_top: int
    sidebar_content_item_margin_bottom: int
    sidebar_content_item_margin_left: int
    sidebar_content_item_margin_right: int

    # OLD TOKENS (kept for backward compatibility)
    dock_border_width: int
    header_padding: int
    toolbar_padding: int
    toolbar_border_width: int
    action_row_radius: int
    action_row_padding_y: int
    action_row_padding_x: int
    input_border_width: int
    input_padding: int


def sidebar_tokens(metrics: Metrics) -> SidebarTokens:
    return SidebarTokens(
        # Sidebar container tokens
        sidebar_container_border_radius=metrics.radius_zero,

        sidebar_container_border_width_top=metrics.border_width_zero,
        sidebar_container_border_width_bottom=metrics.border_width_zero,
        sidebar_container_border_width_left=metrics.border_width_zero,
        sidebar_container_border_width_right=metrics.border_width_zero,

        sidebar_header_border_top_width=metrics.border_width_small,
        sidebar_header_border_bottom_width=metrics.border_width_small,
        sidebar_header_border_left_width=metrics.border_width_small,
        sidebar_header_border_right_width=metrics.border_width_small,

        sidebar_header_padding_top=metrics.padding_medium,
        sidebar_header_padding_bottom=metrics.padding_medium,
        sidebar_header_padding_left=metrics.padding_medium,
        sidebar_header_padding_right=metrics.padding_medium,

        sidebar_header_margin_top=0,
        sidebar_header_margin_bottom=0,
        sidebar_header_margin_left=0,
        sidebar_header_margin_right=0,

        # Sidebar toolbar tokens
        sidebar_toolbar_border_radius=metrics.radius_zero,
        
        sidebar_toolbar_border_top_width=metrics.border_width_zero,
        sidebar_toolbar_border_bottom_width=metrics.border_width_zero,
        sidebar_toolbar_border_left_width=metrics.border_width_zero,
        sidebar_toolbar_border_right_width=metrics.border_width_zero,

        sidebar_toolbar_padding_top=metrics.padding_medium,
        sidebar_toolbar_padding_bottom=metrics.padding_medium,
        sidebar_toolbar_padding_left=metrics.padding_medium,
        sidebar_toolbar_padding_right=metrics.padding_medium,

        sidebar_toolbar_margin_top=0,
        sidebar_toolbar_margin_bottom=0,
        sidebar_toolbar_margin_left=0,
        sidebar_toolbar_margin_right=0,

        sidebar_toolbar_item_x_spacing=metrics.padding_small,
        sidebar_toolbar_item_padding_top=metrics.padding_small,
        sidebar_toolbar_item_padding_bottom=metrics.padding_small,
        sidebar_toolbar_item_padding_left=metrics.padding_small,
        sidebar_toolbar_item_padding_right=metrics.padding_small,

        # Sidebar content container tokens
        sidebar_content_border_radius=metrics.radius_zero,
        
        sidebar_content_border_top_width=metrics.border_width_zero,
        sidebar_content_border_bottom_width=metrics.border_width_zero,
        sidebar_content_border_left_width=metrics.border_width_zero,
        sidebar_content_border_right_width=metrics.border_width_zero,

        sidebar_content_margin_top=0,
        sidebar_content_margin_bottom=0,
        sidebar_content_margin_left=0,
        sidebar_content_margin_right=0,
        
        # Sidebar content item tokens (Common for Settings items and "select a notebook" items in the notebook list)
        sidebar_content_item_border_top_width=metrics.border_width_zero,
        sidebar_content_item_border_bottom_width=metrics.border_width_zero,
        sidebar_content_item_border_left_width=metrics.border_width_zero,
        sidebar_content_item_border_right_width=metrics.border_width_zero,

        sidebar_content_item_x_spacing=metrics.padding_small,

        sidebar_content_item_padding_top=metrics.padding_small,
        sidebar_content_item_padding_bottom=metrics.padding_small,
        sidebar_content_item_padding_left=metrics.padding_small,
        sidebar_content_item_padding_right=metrics.padding_small,

        sidebar_content_item_margin_top=metrics.padding_medium,
        sidebar_content_item_margin_bottom=metrics.padding_medium,
        sidebar_content_item_margin_left=metrics.padding_medium,
        sidebar_content_item_margin_right=metrics.padding_medium,
        

        # OLD TOKENS
        dock_border_width=metrics.border_width,
        header_padding=metrics.padding_medium,
        toolbar_padding=metrics.padding_medium,
        toolbar_border_width=metrics.border_width,
        action_row_radius=metrics.radius_small,
        action_row_padding_y=metrics.padding_extra_small,
        action_row_padding_x=metrics.padding_small,
        input_border_width=metrics.border_width,
        input_padding=metrics.padding_small,
    )


__all__ = ["SidebarTokens", "sidebar_tokens"]
