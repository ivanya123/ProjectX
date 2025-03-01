import flet as ft
from flet_route import Params, Basket


class FridgePage:
    def view(self, page: ft.Page, params: Params, basket: Basket):
        page.title = 'Холодильник'

        return ft.View(
            controls=[
                ft.Text(value='Холодильник'),
                ft.ElevatedButton('Основная страница', on_click=lambda _: page.go('/'))
            ]
        )
