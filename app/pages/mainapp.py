import flet as ft
from flet_route import Params, Basket
from database import *


class LinkContainer(ft.Container):
    def __init__(self, link: str, source, page: ft.Page):
        ft.Container.__init__(self)
        self.expand = True
        self.expand_loose = True
        self.alignment = ft.alignment.center
        self.bgcolor = '#d1c0a8'
        self.border_radius = 10
        self.ink = True
        self.ink_color = '#b3a696'
        self.on_click = lambda _: page.go(link)
        self.content = ft.Image(
            src=source,
            filter_quality=ft.FilterQuality.NONE,
            border_radius=10,
            fit=ft.ImageFit.COVER,
            repeat=ft.ImageRepeat.REPEAT,
            width=self.width
        )


class MainContainer(ft.Container):
    def __init__(self, page: ft.Page):
        ft.Container.__init__(self)
        self.expand = 2
        self.expand_loose = True
        self.alignment = ft.alignment.center
        self.content = ft.Row(
            controls=[
                LinkContainer('/', 'images/recipe.jpg', page),
                LinkContainer('/fridge', 'images/fridge.jpg', page),
                LinkContainer('/products', 'images/product.jpg', page),
                LinkContainer('/add_recipe', 'images/add_recipe.jpg', page),
            ],
            expand=True,
            alignment=ft.alignment.center,
            spacing=0
        )


class MainApp:

    def __init__(self):
        self.all_recipes: list[Recipes] = reading_recipes()
        self.all_products: list[Products] = reading_products()
        self.all_categories: list[Categories] = reading_categories()
        self.main_view = None
        self.controls = None

    def view(self, page: ft.Page, params: Params, basket: Basket):
        self.all_recipes: list[Recipes] = reading_recipes()
        self.all_products: list[Products] = reading_products()
        self.all_categories: list[Categories] = reading_categories()
        page.title = 'Кулинарная книга Ивана и Полины'
        self.controls = [
            MainContainer(page),
            ft.Container(expand=18),
        ]
        self.main_view = ft.View(
            controls=self.controls,
            padding=ft.padding.all(0),
            spacing=0
        )

        return self.main_view

    def update_data(self, obj=None):
        if obj is None:
            self.all_recipes = reading_recipes()
            self.all_products = reading_products()
            self.all_categories = reading_categories()
        else:
            if isinstance(obj, Recipes):
                self.all_recipes = reading_recipes()
            elif isinstance(obj, Products):
                self.all_products = reading_products()
            elif isinstance(obj, Categories):
                self.all_categories = reading_categories()


