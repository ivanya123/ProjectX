import flet as ft
from flet_route import Params, Basket
from app.pages.mainapp import MainApp


class AddRecipe(MainApp):
    def view(self, page: ft.Page, params: Params, basket: Basket):
        MainApp.view(self, page, params, basket)
        container = self.controls[-1]
        container.image = ft.DecorationImage(
            src="images/add_recipe_background.webp", repeat=ft.ImageRepeat.REPEAT
        )


        return self.main_view