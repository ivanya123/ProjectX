import flet as ft
from flet_route import Routing, path
from app.pages.mainapp import MainApp
from app.pages.fridge import FridgePage


class Router:
    def __init__(self, page: ft.Page):
        self.page = page
        self.app_routes = [
            path(url="/", clear=True, view=MainApp().view),
            path(url="/fridge", clear=False, view=FridgePage().view)
        ]

        Routing(
            page=self.page,
            app_routes=self.app_routes
        )
        self.page.go(self.page.route)
