"""Text input component and labeled field wrapper."""
from __future__ import annotations

import flet as ft

from ..theme import Space, Radius


def TextInput(
    P,
    hint: str = "",
    value: str = "",
    width=None,
    on_change=None,
    disabled: bool = False,
    expand: bool = False,
) -> ft.Control:
    """A styled text field.

    Background is always the page color (no gray fill), so it matches
    Dropdowns and Containers used across the app. When disabled, we use
    `read_only` and a very subtle opacity, keeping the text readable.
    """
    field = ft.TextField(
        hint_text=hint,
        value=value,
        width=width,
        on_change=on_change,
        read_only=disabled,
        height=46,
        bgcolor=P["bg"],
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
    if disabled:
        field.opacity = 0.9
    if expand:
        return ft.Container(content=field, expand=True)
    return field


def LabeledField(P, label: str, control: ft.Control) -> ft.Control:
    """A small label above a control that stretches to fill the row."""
    return ft.Column(
        [
            ft.Text(
                label,
                color=P["text_muted"],
                size=12,
                weight=ft.FontWeight.W_500,
            ),
            ft.Container(height=Space.xs),
            control,
        ],
        spacing=0,
        tight=True,
        expand=True,
    )