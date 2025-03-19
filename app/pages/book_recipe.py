import flet as ft
from app.pages.mainapp import MainApp
from app.styles import *
from app.utils import desc_to_list, type_to_suffix
from database import *


def amount_in_fridge(product: Products, all_fridge: list[Fridge]):
    for fridge in all_fridge:
        if fridge.products.id == product.id:
            return fridge.amount


class ContainerRecipe(ft.Container):
    def __init__(self, recipe: Recipes = None):
        super().__init__()
        self.recipe = recipe
        self.all_fridge: list[Fridge] = reading_fridge()
        self.current_desc = 0
        self.expand = True
        self.text_name = ft.Text(style=MAIN_STYLE_TEXT, value=self.recipe.name)
        self.description = ft.Text(style=MAIN_STYLE_TEXT,
                                   value=desc_to_list(self.recipe.description)[0])
        self.content = ft.Column(
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    expand=1,
                    controls=[
                        ft.Container(
                            blur=ft.Blur(10, 15, tile_mode=ft.BlurTileMode.CLAMP),
                            expand=5,
                            content=self.text_name,
                        ),
                        ft.TextButton('Выбрать рецепт', on_click=lambda _: self.choice_recipe(),
                                      expand=1, style=ft.ButtonStyle(text_style=MAIN_STYLE_TEXT, color=ft.Colors.WHITE))
                    ]
                ),
                ft.Row(
                    expand=5,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Container(expand=1, on_click=self.previous_desc, content=ft.Icon(ft.icons.ARROW_BACK),
                                     height=500),

                        ft.Container(
                            expand=5,
                            height=500,
                            blur=ft.Blur(10, 15, tile_mode=ft.BlurTileMode.CLAMP),
                            content=self.description
                        ),
                        ft.Container(expand=1, on_click=self.next_desc, content=ft.Icon(ft.icons.ARROW_FORWARD),
                                     height=500)
                    ]
                ),
                ft.Column(
                    height=300,
                    scroll=ft.ScrollMode.ALWAYS,
                    controls=[
                        RowComparison(product, amount_in_fridge(product[0], self.all_fridge)) for product in
                        self.recipe.product_list
                    ]
                )
            ]
        )

    def choice_recipe(self):
        pass

    def next_desc(self, event):
        if self.description.value != desc_to_list(self.recipe.description)[-1]:
            self.description.value = desc_to_list(self.recipe.description)[self.current_desc + 1]
            self.current_desc += 1
            self.update()

    def previous_desc(self, event):
        if self.description.value != desc_to_list(self.recipe.description)[0]:
            self.description.value = desc_to_list(self.recipe.description)[self.current_desc - 1]
            self.current_desc -= 1
            self.update()


class RowComparison(ft.Row):
    def __init__(self, product: tuple[Products, float], amount_in_fridge: float):
        super().__init__()
        self.product = product[0]
        self.amount_recipe = product[1]
        self.text_change = ft.Text(style=MAIN_STYLE_TEXT, expand=1)
        self.alignment = ft.MainAxisAlignment.START
        try:
            if amount_in_fridge >= self.amount_recipe:
                self.text_change.color = ft.Colors.GREEN
                self.text_change.value = "Хватает"
            else:
                self.text_change.color = ft.Colors.RED
                self.text_change.value = f"Не хватает: {self.amount_recipe - amount_in_fridge}"
        except TypeError:
            if amount_in_fridge is None:
                self.text_change.color = ft.Colors.RED
                self.text_change.value = (f"Не хватает: {self.amount_recipe}"
                                          f" {type_to_suffix(self.product.product_type)} (Нету в холодильнике)")
        self.controls = [
            ft.Text(value=self.product.name, style=MAIN_STYLE_TEXT, expand=1),
            ft.Text(value=f"Нужно: {self.amount_recipe} {type_to_suffix(self.product.product_type)}",
                    style=MAIN_STYLE_TEXT,
                    expand=1),
            ft.Text(value=f"Есть: {amount_in_fridge} {type_to_suffix(self.product.product_type)}",
                    style=MAIN_STYLE_TEXT, expand=1),
            self.text_change
        ]


class BookRecipe(MainApp):
    def view(self, page, params, basket):
        MainApp.view(self, page, params, basket)
        container = self.controls[-1]
        container.image = ft.DecorationImage(
            src="images/recipe_background.webp",
            repeat=ft.ImageRepeat.REPEAT,
        )
        container.content = ft.Column(
            expand=True,
            controls=[
                ContainerRecipe(self.all_recipes[0])
            ]
        )
        return self.main_view
