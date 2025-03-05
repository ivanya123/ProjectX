import time

import flet as ft
from flet.core.form_field_control import InputBorder
from flet_route import Params, Basket

from app.pages.mainapp import MainApp


def add_recipe():
    pass


class NewTabs(ft.Tabs):

    def new_index(self):
        self.selected_index = len(self.tabs) - 2
        self.update()


row_add = ft.Row(
    expand=1,
    alignment=ft.MainAxisAlignment.CENTER,
    controls=[
        ft.Container(expand=1, blur=ft.Blur(1, 50, tile_mode=ft.BlurTileMode.MIRROR),
                     content=ft.Text("Добавить рецепт", color=ft.Colors.BLACK,
                                     italic=True, text_align=ft.TextAlign.CENTER,
                                     size=25, expand=1, height=100),
                     on_click=lambda _: add_recipe(), ink=True, ink_color='#b3a696')
    ],

)

container_name = ft.Container(expand=1,
                              content=ft.TextField(hint_text='Рецепт: ',
                                                   color=ft.colors.WHITE70, text_style=ft.TextStyle(italic=True,
                                                                                                    size=15),
                                                   prefix_style=ft.TextStyle(italic=True, color=ft.colors.WHITE24,
                                                                             size=15),
                                                   border=InputBorder.NONE,
                                                   multiline=True,
                                                   max_lines=2),
                              blur=ft.Blur(1, 50, tile_mode=ft.BlurTileMode.CLAMP),
                              alignment=ft.alignment.top_right,
                              border=ft.border.all(1, '#b3a696'),
                              border_radius=5)
row_high = ft.Row(
    alignment=ft.MainAxisAlignment.START,
    controls=[container_name],
    expand=1
)

tab_add = ft.Tab(icon=ft.icons.ADD)
tab_minus = ft.Tab(icon=ft.icons.REMOVE)


def new_tab_description(number: int) -> ft.Tab:
    return ft.Tab(text=f'{number}',
                  content=ft.Container(
                      content=ft.TextField(multiline=True, expand=True, min_lines=5, border=InputBorder.NONE,
                                           label=f'{number} этап', prefix_text=f'{number}. '),
                      blur=ft.Blur(5, 10, tile_mode=ft.BlurTileMode.CLAMP)
                  ))


def change_tab(e: ft.ControlEvent):
    tabs: NewTabs = e.control
    # Если выбрана вкладка "добавить" (последняя)

    if tabs.selected_index == len(tabs.tabs) - 2:
        tabs.tabs[-2] = new_tab_description(len(tabs.tabs) - 1)
        tabs.tabs[-1] = tab_add
        tabs.tabs.append(tab_minus)
        tabs.update()
        for tab in tabs.tabs:
            tab.update()
        tabs.page.update()
    elif tabs.selected_index == len(tabs.tabs) - 1:
        if len(tabs.tabs) == 3:
            tabs.selected_index = 0
            tabs.update()
            return
        tabs.tabs.pop()
        tabs.tabs[-2] = tab_add
        tabs.tabs[-1] = tab_minus
        tabs.update()
        for tab in tabs.tabs:
            tab.update()


class RowProduct(ft.Row):
    pass


recipe_product = ft.Container(
    expand=1,
    border=ft.border.all(1, '#b3a696'),
    content=ft.Column(
        expand=True,
        on_scroll_interval=0,
        scroll="always",
        controls=[
            RowProduct(
                expand=1,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[ft.Text(f'Продукт_{i}', size=15, expand=2), ft.TextField(expand=1)]
            ) for i in range(20)]
    )
)

all_products = ft.Container(
    expand=1,
    content=ft.Column(
        expand=True,
        controls=[
            ft.Container(
                expand=2,
                content=ft.Row(
                    expand=1,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[ft.Dropdown(
                        expand=True,
                        options=[
                            ft.DropdownOption(key=f'Категория_{i}', content=ft.Text(f'Категория_{i}')) for i in
                            range(20)
                        ]
                    ), ft.TextField(expand=1, hint_text='Фильтрация по названию', label='Фильтр')]
                )
            ),
            ft.Column(
                expand=10,
                scroll="always",
                controls=[ft.Row(
                    expand=1,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[ft.Text(f'Продукт_{i}', size=15, expand=2), ft.Button(icon=ft.icons.ADD, text='Добавить')]
                ) for i in range(20)]
            )
        ]
    )
)

row_add_product = ft.Row(
    expand=12,
    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    controls=[
        recipe_product,
        all_products
    ]
)


class AddRecipe(MainApp):
    def view(self, page: ft.Page, params: Params, basket: Basket):
        MainApp.view(self, page, params, basket)
        container = self.controls[-1]
        container.image = ft.DecorationImage(
            src="images/add_recipe_background.webp", repeat=ft.ImageRepeat.REPEAT
        )

        self.tabs = NewTabs(tabs=[new_tab_description(1),
                                  tab_add, tab_minus],
                            expand=True,
                            on_change=change_tab
                            )

        container.content = ft.Column(
            controls=[row_high,
                      ft.Row(expand=6, controls=[self.tabs]),
                      row_add_product,
                      row_add]
        )

        return self.main_view
