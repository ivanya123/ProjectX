from collections.abc import Callable

import flet as ft
from flet_route import Params, Basket

from app.pages import FakeCategory, categories, FakeProduct, fake_products
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
        self.padding = 0

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
    def __init__(self, value: str = None):
        super().__init__(content=ft.Row())
        self.expand = 1
        self.content = ft.Row(
            spacing=0,
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            controls=[
                ft.Radio(value='весовой', label='Весовой', label_style=MAIN_STYLE_TEXT),
                ft.Radio(value='штучный', label='Штучный', label_style=MAIN_STYLE_TEXT),
                ft.Radio(value='жидкость', label='Жидкий', label_style=MAIN_STYLE_TEXT)
            ]
        )
        self.value = value


class ColumnAddProduct(ft.Column):
    def __init__(self):
        super().__init__()
        self.id_product = None
        self.border = ft.border.all(3, ft.colors.GREEN_900)
        self.expand = 3
        self.alignment = ft.MainAxisAlignment.SPACE_EVENLY
        self.radio_type = RadioType()
        self.in_category = ColumnCategory()
        self.all_category = ColumnCategory(
            categories_=[ContainerCategory(category, self.go_category) for category in categories],
            right=True
        )
        self.text_name = ft.TextField(
            hint_text='Название', hint_style=MAIN_STYLE_TEXT,
            text_style=MAIN_STYLE_TEXT
        )
        self.controls = [
            ft.Container(
                expand=2,
                blur=ft.Blur(10, 15, tile_mode=ft.BlurTileMode.CLAMP),
                content=self.text_name,
            ),
            ft.Container(
                expand=2,
                blur=ft.Blur(10, 15, tile_mode=ft.BlurTileMode.CLAMP),
                content=self.radio_type
            ),
            ft.Row(
                expand=3,
                controls=[
                    ft.Container(
                        expand=3,
                        border=ft.border.all(1, ft.colors.GREY_600),
                        border_radius=ft.border_radius.all(5),
                        content=ft.Column(
                            spacing=1,
                            controls=[
                                ft.Text('Выбранные категории:', style=MAIN_STYLE_TEXT),
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
                                ft.Text('Выберите категории:', style=MAIN_STYLE_TEXT),
                                self.all_category
                            ]
                        )
                    )
                ]),
            ft.Row(
                controls=[
                    ft.IconButton(ft.Icons.ADD, on_click=self.add_click),
                    ft.IconButton(ft.Icons.CLEAR, on_click=self.clear_click)
                ]
            )

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
            id=self.id_product,
            name=self.text_name.value,
            type_=self.radio_type.value,
            category=[category.category for category in
                      self.in_category.controls] if self.in_category.controls else None
        )
        print(new_product)

    def clear_click(self, _: ft.ControlEvent):
        self.id_product = None
        self.text_name.value = ''
        self.in_category.controls = []
        self.all_category.controls = [ContainerCategory(category, self.go_category) for category in categories]
        self.radio_type.value = None

        self.parent.border=ft.border.all(4, ft.colors.GREY_600)
        self.parent.update()

    def edit_product(self, product: FakeProduct):
        self.id_product = product.id
        self.text_name.value = product.name
        self.radio_type.value = product.type_
        self.in_category.controls = (
            [ContainerCategory(category, self.go_category) for category in product.category] if product.category else []
        )
        self.all_category.controls = (
            [ContainerCategory(category, self.go_category)
             for category in categories if category not in product.category] if product.category else [
                ContainerCategory(category, self.go_category) for category in categories
            ]
        )
        self.radio_type.value = product.type_

        self.parent.border = ft.border.all(3, ft.colors.BLUE_900)
        self.parent.update()


class ProductRow(ft.Container):
    def __init__(self, product: FakeProduct, edit_click: Callable):
        super().__init__()
        self.data = product
        self.expand = 1
        self.blur = ft.Blur(10, 15, tile_mode=ft.BlurTileMode.CLAMP)
        self.category_text = ', '.join(
            category.name for category in product.category) if product.category else 'Без категории'
        self.content = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(value=f'{product.id}: {product.name}', style=MAIN_STYLE_TEXT),
                ft.Text(value=product.type_, style=MAIN_STYLE_TEXT),
                ft.Text(value=self.category_text, style=MAIN_STYLE_TEXT),
                ft.TextButton(on_click=edit_click, icon=ft.icons.EDIT),
                ft.TextButton(on_click=self.delete_click, icon=ft.icons.DELETE, icon_color=ft.colors.RED_400)
            ]
        )

    def delete_click(self, _: ft.ControlEvent):
        pass


class AllProducts(ft.Container):
    def __init__(self, products: list[FakeProduct] = None, edit_click: Callable = None):
        super().__init__()
        self.expand = 6
        self.padding = 10
        self.blur = ft.Blur(10, 15, tile_mode=ft.BlurTileMode.CLAMP)
        self.content = ft.Column(
            scroll=ft.ScrollMode.ALWAYS,
            controls=[ProductRow(product, edit_click) for product in products] if products else []
        )


class Products(MainApp):
    def __init__(self):
        self.all_products = None
        self.column_add_product: ColumnAddProduct = None

    def view(self, page: ft.Page, params: Params, basket: Basket):
        MainApp.view(self, page, params, basket)
        container = self.controls[-1]
        container.image = ft.DecorationImage(
            src="images/products_background.webp", repeat=ft.ImageRepeat.REPEAT
        )
        self.column_add_product: ColumnAddProduct = ColumnAddProduct()
        self.all_products = AllProducts(products=fake_products, edit_click=self.edit_click)

        container.content = ft.Column(
            controls=[
                self.all_products,
                ft.Container(content=self.column_add_product, expand=6, border_radius=ft.border_radius.all(5),
                             border=ft.border.all(4, ft.colors.GREY_600)),
                ft.Container(expand=6)
            ]
        )

        return self.main_view

    def edit_click(self, e: ft.ControlEvent):
        container_product: ProductRow = e.control.parent.parent
        self.column_add_product.edit_product(container_product.data)
