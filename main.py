import flet as ft
from database import new_bd

new_bd()

from app.router import Router


def main(page: ft.Page):
    page.fonts = {
        'Pattaya': 'fonts/Pattaya-Regular.ttf',
        'Oranienbaum': 'fonts/Oranienbaum-Regular.ttf',
        'Caveat': 'fonts/Caveat-VariableFont_wght.ttf'
    }
    page.theme = ft.Theme(font_family='Caveat')

    Router(page)


if __name__ == '__main__':
    ft.app(target=main, assets_dir="app/assets", port=5000)
