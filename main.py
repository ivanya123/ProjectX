import flet as ft
from app.router import Router


def main(page: ft.Page):
    Router(page)


if __name__ == '__main__':
    ft.app(target=main, view=ft.WEB_BROWSER, assets_dir="assets", port=5050)

