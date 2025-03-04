import flet as ft
from flet_route import Routing, path
from app.pages import BookRecipe, Products, FridgePage, AddRecipe


class Router:
    def __init__(self, page: ft.Page):
        self.page = page
        self.app_routes = [
            path(url="/", clear=True, view=BookRecipe().view),
            path(url="/fridge", clear=False, view=FridgePage().view),
            path(url='/products', clear=False, view=Products().view),
            path(url='/add_recipe', clear=False, view=AddRecipe().view),
        ]

        Routing(
            page=self.page,
            app_routes=self.app_routes
        )
        self.page.go(self.page.route)
