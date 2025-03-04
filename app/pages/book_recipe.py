import flet as ft
from flet_route import Params, Basket
from app.pages.mainapp import MainApp


class BookRecipe(MainApp):
    def view(self, page, params, basket):
        MainApp.view(self, page, params, basket)
        container = self.controls[-1]
        container.image = ft.DecorationImage(
            src="images/recipe_background.webp",
            repeat=ft.ImageRepeat.REPEAT,
        )
        return self.main_view
