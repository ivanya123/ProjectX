import flet as ft
from flet_route import Params, Basket


class MainApp:
    def view(self, page: ft.Page, params: Params, basket: Basket):
        page.title = 'Наш хололдильник с книгой рецептов'

        return ft.View(
            controls=[
                ft.Text(value='Холодильник с книгой рецептов'),
                ft.ElevatedButton('Cтраница холодильника', on_click=lambda _: page.go('/fridge'))
            ]
        )
