from collections.abc import Callable

import flet as ft
from flet_route import Params, Basket

from app.pages import FakeCategory, categories, FakeProduct
from app.pages.mainapp import MainApp

from app.styles import *


class ContainerCategory(ft.Container):
    def __init__(self, category: FakeCategory, func_category: Callable):
        super().__init__()
        self.category = category
        self.blur = ft.Blur(10, 15, tile_mode=ft.BlurTileMode.CLAMP)
        self.content = ft.Text(category.name, style=MAIN_STYLE_TEXT)
        self.on_click = func_category
        self.ink = True

    @property
    def data_(self):
        return self.category


class ColumnCategory(ft.Column):
    def __init__(self, categories_: list[ContainerCategory] = None, right: bool = False):
        super().__init__()
        if categories_ is None:
            categories_ = []
        self.controls = categories_
        self.spacing = 3
        self.scroll = ft.ScrollMode.ALWAYS
        self.expand = 1
        self.right = right
        self.wrap = True


class FilterCategory(ft.Container):
    def __init__(self, change: Callable):
        super().__init__()
        self.expand = 1
        self.text_ = ft.TextField(hint_text='Фильтр по названию', hint_style=MAIN_STYLE_TEXT,
                                  text_style=MAIN_STYLE_TEXT, on_change=change)
        self.content = self.text_


class RadioType(ft.RadioGroup):
    def __init__(self):
        super().__init__(content=ft.Row())
        self.expand = 1
        self.content = ft.Column(
            spacing=2,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Radio(value='весовой', label='Весовой', label_style=LABEL_STYLE_TEXT),
                ft.Radio(value='штучный', label='Штучный', label_style=LABEL_STYLE_TEXT),
                ft.Radio(value='жидкость', label='Жидкий', label_style=LABEL_STYLE_TEXT)
            ]
        )


class RowProduct(ft.Row):
    def __init__(self):
        super().__init__()
        self.expand = 3
        self.alignment = ft.MainAxisAlignment.SPACE_EVENLY
        self.radio_type = RadioType()
        self.in_category = ColumnCategory()
        self.all_category = ColumnCategory(
            categories_=[ContainerCategory(category, self.go_category) for category in categories],
            right=True
        )
        self.text_name = ft.TextField(
            hint_text='Название', hint_style=LABEL_STYLE_TEXT,
            text_style=LABEL_STYLE_TEXT
        )
        self.controls = [
            ft.Container(
                expand=1,
                blur=ft.Blur(10, 15, tile_mode=ft.BlurTileMode.CLAMP),
                content=self.text_name,
            ),
            ft.Container(
                expand=1,
                blur=ft.Blur(10, 15, tile_mode=ft.BlurTileMode.CLAMP),
                content=self.radio_type
            ),
            ft.Container(
                expand=3,
                border=ft.border.all(1, ft.colors.GREY_600),
                border_radius=ft.border_radius.all(5),
                content=ft.Column(
                    spacing=1,
                    controls=[
                        ft.Text('Выбранные категории:', style=LABEL_STYLE_TEXT),
                        self.in_category
                    ]
                )
            ),
            ft.Container(
                expand=3,
                border=ft.border.all(1, ft.colors.GREY_600),
                border_radius=ft.border_radius.all(5),
                content=ft.Column(
                    spacing=1,
                    controls=[
                        ft.Text('Выберите категории:', style=LABEL_STYLE_TEXT),
                        self.all_category
                    ]
                )
            ),
            ft.IconButton(ft.Icons.ADD, on_click=self.add_click)

        ]

    def go_category(self, e: ft.ControlEvent):
        container_category: ContainerCategory = e.control
        parent: ColumnCategory = container_category.parent
        if parent.right:
            self.in_category.controls.append(ContainerCategory(container_category.category, self.go_category))
            self.all_category.controls.remove(container_category)
        elif not parent.right:
            self.all_category.controls.append(ContainerCategory(container_category.category, self.go_category))
            self.in_category.controls.remove(container_category)
        self.update()

    def add_click(self, _: ft.ControlEvent):
        new_product: FakeProduct = FakeProduct(
            name=self.text_name.value,
            type_=self.radio_type.value,
            category=[category.category for category in
                      self.in_category.controls] if self.in_category.controls else None
        )
        print(new_product)


class Products(MainApp):
    def view(self, page: ft.Page, params: Params, basket: Basket):
        MainApp.view(self, page, params, basket)
        container = self.controls[-1]
        container.image = ft.DecorationImage(
            src="images/products_background.webp", repeat=ft.ImageRepeat.REPEAT
        )
        container.content = ft.Column(
            controls=[
                RowProduct(),
                ft.Container(expand=6),
                ft.Container(expand=6)
            ]
        )
        return self.main_view
