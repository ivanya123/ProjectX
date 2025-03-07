import math

import flet as ft
from flet_route import Routing, path
from app.pages import BookRecipe, Products, FridgePage, AddRecipe
from app.styles import *


class Router:
    def __init__(self, page: ft.Page):
        self.page = page
        self.app_routes = [
            path(url="/", clear=True, view=BookRecipe().view),
            path(url="/fridge", clear=False, view=FridgePage().view),
            path(url='/products', clear=False, view=Products().view),
            path(url='/add_recipe', clear=False, view=AddRecipe().view),
        ]
        MAIN_STYLE_TEXT.size = min(math.ceil(page.width / 20), 27) + 1
        LABEL_STYLE_TEXT.size = min(math.ceil(page.width / 40), 16) + 1
        page.theme_mode = ft.ThemeMode.DARK

        def change_resize(e: ft.WindowResizeEvent):
            MAIN_STYLE_TEXT.size = min(math.ceil(e.width / 20), 27) + 1
            LABEL_STYLE_TEXT.size = min(math.ceil(e.width / 40), 16) + 1
            page.update()

        page.on_resized = change_resize

        Routing(
            page=self.page,
            app_routes=self.app_routes
        )
        self.page.go(self.page.route)
