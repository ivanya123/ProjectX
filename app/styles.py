import flet as ft

__all__ = [
    "MAIN_STYLE_TEXT",
    "LABEL_STYLE_TEXT",
    "TAB_STYLE_TEXT"
]

MAIN_STYLE_TEXT = ft.TextStyle(
    color=ft.Colors.WHITE,
    size=28
)
LABEL_STYLE_TEXT = ft.TextStyle(
    italic=True, color=ft.Colors.WHITE,
    size=16, weight=ft.FontWeight.W_700
)
TAB_STYLE_TEXT = ft.TextStyle(
    color=ft.Colors.WHITE, size=28, weight=ft.FontWeight.W_900
)
