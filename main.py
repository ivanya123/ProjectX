import flet as ft
from app.router import Router
from database.create import new_bd



def main(page: ft.Page):
    new_bd()
    page.fonts = {
        'Pattaya': 'fonts/Pattaya-Regular.ttf',
        'Oranienbaum': 'fonts/Oranienbaum-Regular.ttf',
        'Caveat': 'fonts/Caveat-VariableFont_wght.ttf'
    }
    page.theme = ft.Theme(font_family='Caveat')

    Router(page)


if __name__ == '__main__':
    ft.app(target=main, assets_dir="assets")

