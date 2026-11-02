"""Settings — structured preferences."""
from __future__ import annotations

import flet as ft
from pathlib import Path

from ..theme import Space, Radius, Type, BP
from ..components import (
    SectionCard, LabeledField, TextInput, SecondaryButton,
)
from ..components.action_button import ActionButton
from ._scaffold import page_scaffold


def _row_setting(
    P,
    title: str,
    subtitle: str,
    control: ft.Control,
    is_mobile: bool = False,
) -> ft.Control:
    """A settings row — title + subtitle on left, control on right.

    On mobile, only input fields stack vertically; icons stay inline.
    """
    left_col = ft.Column(
        [
            ft.Text(title, color=P["text"], size=15, weight=ft.FontWeight.W_600),
            ft.Container(height=4),
            ft.Text(
                subtitle, color=P["text_muted"], size=13,
                weight=ft.FontWeight.W_400, max_lines=None,
                overflow=ft.TextOverflow.ELLIPSIS,
                no_wrap=False,
            ),
        ],
        spacing=0, tight=True, expand=True,
    )

    # Detect small icons so they stay inline on mobile as well.
    is_icon = isinstance(control, ft.Icon) or (
        isinstance(control, ft.Container)
        and control.width is not None
        and control.width <= 100
    )

    if not is_mobile or is_icon:
        return ft.Container(
            content=ft.Row(
                [left_col, control],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=Space.md,
            ),
            padding=ft.Padding.symmetric(vertical=Space.md),
        )

    return ft.Container(
        content=ft.Column(
            [
                left_col,
                ft.Container(height=Space.md),
                ft.Row(
                    [control],
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
            spacing=0, tight=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        ),
        padding=ft.Padding.symmetric(vertical=Space.md),
    )


def _divider(P):
    return ft.Container(
        height=1,
        bgcolor=P["border"],
        margin=ft.Margin.symmetric(vertical=Space.sm),
    )


def build_settings(P, state, handlers, page_width=1200):
    is_mobile = page_width < BP.md

    # ---- Appearance ----
    current_mode = getattr(state, "theme_mode", "auto")

    theme_dropdown = ft.Dropdown(
        value=current_mode,
        options=[
            ft.dropdown.Option(key="auto", text="Auto (system)"),
            ft.dropdown.Option(key="light", text="Light"),
            ft.dropdown.Option(key="dark", text="Dark"),
        ],
        on_select=lambda e: handlers["set_theme"](e.control.value or "auto"),
        height=46,
        bgcolor=P["bg"],  # Match the rest of the fields
        color=P["text"],
        text_style=ft.TextStyle(color=P["text"], size=15),
        content_padding=ft.Padding.symmetric(horizontal=Space.md, vertical=0),
        border={
            ft.ControlState.DEFAULT: ft.OutlineInputBorder(
                border_radius=Radius.lg,
                side=ft.BorderSide(1, P["border"]),
            ),
            ft.ControlState.FOCUSED: ft.OutlineInputBorder(
                border_radius=Radius.lg,
                side=ft.BorderSide(1, P["primary"]),
            ),
        },
    )

    theme_dropdown_wrapper = ft.Container(
        content=theme_dropdown,
        expand=is_mobile,
        width=None if is_mobile else 200,
    )

    appearance_card = SectionCard(
        P, dark=state.dark,
        title="Appearance",
        content=ft.Column(
            [
                _row_setting(
                    P,
                    "Theme",
                    "Choose light, dark, or follow the system.",
                    theme_dropdown_wrapper,
                    is_mobile=is_mobile,
                ),
            ],
            spacing=0, tight=True,
        ),
    )

    # ---- Server ----
    device_field = TextInput(
        P, hint="Device name", value=state.device_name,
        on_change=lambda e: handlers["set_device_name"](e.control.value or ""),
    )
    if state.server_running:
        device_field.read_only = True
        device_field.opacity = 0.9
    if state.server_running:
        device_field.read_only = True
        device_field.opacity = 0.6
    
    device_field_wrapper = ft.Container(
        content=device_field,
        expand=is_mobile,
        width=None if is_mobile else 220,
    )

    default_port_field = TextInput(
        P, hint="8000", value=state.port or "8000",
        on_change=lambda e: handlers["set_port"](e.control.value),
    )
    if state.server_running:
        default_port_field.read_only = True
        default_port_field.opacity = 0.9
    
    if state.server_running:
        default_port_field.read_only = True
        default_port_field.opacity = 0.6

    default_port_field_wrapper = ft.Container(
        content=default_port_field,
        expand=is_mobile,
        width=None if is_mobile else 140,
    )

    server_card = SectionCard(
        P, dark=state.dark,
        title="Server",
        content=ft.Column(
            [
                _row_setting(
                    P,
                    "Device name",
                    "Shown in the web page header.",
                    device_field_wrapper,
                    is_mobile=is_mobile,
                ),
                _divider(P),
                _row_setting(
                    P,
                    "Default port",
                    "Used when starting the server.",
                    default_port_field_wrapper,
                    is_mobile=is_mobile,
                ),
            ],
            spacing=0, tight=True,
        ),
    )

    # ---- About ----
    _here = Path(__file__).resolve()
    _asset_candidates = [
        _here.parent.parent.parent / "assets",
        _here.parent.parent.parent.parent / "assets",
        Path.cwd() / "assets",
        Path.cwd() / "src" / "assets",
    ]
    assets_dir = next(
        (p for p in _asset_candidates if p.is_dir() and (p / "logo_dark.png").exists()),
        None,
    )

    if assets_dir:
        logo_filename = "logo_dark.png" if state.dark else "logo_light.png"
        about_icon = ft.Container(
            content=ft.Image(
                src=str(assets_dir / logo_filename),
                width=40, height=40,
                fit=ft.BoxFit.CONTAIN,
            ),
            width=56, height=56,
            bgcolor=P["surface_2"],
            border=ft.Border.all(1, P["border"]),
            border_radius=Radius.md,
            alignment=ft.Alignment.CENTER,
            padding=ft.Padding.all(6),
        )
    else:
        about_icon = ft.Icon(ft.Icons.FOLDER_SHARED_ROUNDED, size=40, color=P["text_muted"])

    about_card = SectionCard(
        P, dark=state.dark,
        title="About",
        content=ft.Column(
            [
                _row_setting(
                    P,
                    "BitBeagle",
                    "Version 1.0.0 — Local file sharing.",
                    about_icon,
                    is_mobile=is_mobile,
                ),
                _divider(P),
                _row_setting(
                    P,
                    "Share directory",
                    state.share_dir_display,
                    ft.Container(),
                    is_mobile=is_mobile,
                ),
            ],
            spacing=0, tight=True,
        ),
    )

    # ---- Open Source ----
    open_source_card = SectionCard(
        P, dark=state.dark,
        title="Open Source",
        content=ft.Column(
            [
                _row_setting(
                    P,
                    "BitBeagle on GitHub",
                    "Free & open source under the MIT license. Star it, fork it, contribute.",
                    ft.Container(
                        content=ft.Icon(ft.Icons.CODE_ROUNDED, size=22, color=P["text_muted"]),
                        width=40, height=40,
                        alignment=ft.Alignment.CENTER,
                    ),
                    is_mobile=is_mobile,
                ),
                _divider(P),
                _row_setting(
                    P,
                    "Report a bug",
                    "Found an issue? Open a ticket on GitHub.",
                    ft.Container(
                        content=ft.Icon(ft.Icons.BUG_REPORT_ROUNDED, size=22, color=P["text_muted"]),
                        width=40, height=40,
                        alignment=ft.Alignment.CENTER,
                    ),
                    is_mobile=is_mobile,
                ),
                ft.Container(height=Space.md),
                ft.Column(
                    [
                        ft.Container(
                            content=ActionButton(
                                P, "View on GitHub",
                                icon=ft.Icons.OPEN_IN_NEW_ROUNDED,
                                on_click=handlers["open_github"],
                                kind="secondary",
                            ),
                            expand=True,
                        ),
                        ft.Container(
                            content=ActionButton(
                                P, "Report an issue",
                                icon=ft.Icons.BUG_REPORT_ROUNDED,
                                on_click=handlers["open_issues"],
                                kind="secondary",
                            ),
                            expand=True,
                        ),
                    ],
                    spacing=Space.sm,
                    tight=True,
                ),
            ],
            spacing=0, tight=True,
        ),
    )

    body = ft.Column(
        [
            appearance_card,
            ft.Container(height=Space.md),
            server_card,
            ft.Container(height=Space.md),
            about_card,
            ft.Container(height=Space.md),
            open_source_card,
        ],
        spacing=0,
        tight=True,
    )

    return page_scaffold(
        P,
        title="Settings",
        subtitle="Preferences and information",
        content=body,
        page_width=page_width,
    )