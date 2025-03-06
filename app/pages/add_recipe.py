import random
from collections.abc import Callable
from dataclasses import dataclass
from typing import Optional

import flet as ft
from flet.core.form_field_control import InputBorder
from flet_route import Params, Basket

from app.pages.mainapp import MainApp


def add_recipe():
    pass


row_add = ft.Row(
    expand=1,
    alignment=ft.MainAxisAlignment.CENTER,
    controls=[
        ft.Container(expand=1, blur=ft.Blur(1, 50, tile_mode=ft.BlurTileMode.MIRROR),
                     content=ft.Text("Добавить рецепт", color=ft.Colors.BLACK,
                                     italic=True, text_align=ft.TextAlign.CENTER,
                                     size=25, expand=1, height=100),
                     on_click=lambda _: add_recipe(), ink=True, ink_color='#b3a696')
    ]
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


@dataclass
class FakeProduct:
    id: int
    name: str
    type: str = 'весовой'
    category: Optional[list['FakeCategory']] = None


@dataclass
class FakeCategory:
    id: int
    name: str
    products: Optional[list[FakeProduct]] = None


categories = [
    FakeCategory(1, 'молочка'),
    FakeCategory(2, 'мясная'),
    FakeCategory(3, 'овощная'),
    FakeCategory(4, 'закуски')
]

fake_products = [FakeProduct(i, f'Продукт_{i}', 'весовой', [random.choice(categories)]) for i in range(50)]


class FilterRow(ft.Row):
    def __init__(self, change_filter: Callable):
        super().__init__()
        self.expand = 2
        self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        self.controls_ = [ft.DropdownOption(key=0, content=ft.Text('Все категории'), text='Все')]
        self.controls_.extend([ft.DropdownOption(key=f'{category.id}',
                                                 content=ft.Text(f'{category.name}'),
                                                 text=f'{category.name}')
                               for category in categories])
        self.dropdown = ft.Dropdown(
            expand=True,
            options=self.controls_,
            on_change=change_filter
        )
        self.textfield = ft.TextField(expand=1, hint_text='Фильтрация по названию', label='Фильтр',
                                      on_change=change_filter)
        self.controls: list[ft.Dropdown, ft.TextField] = [
            self.dropdown,
            self.textfield
        ]

    @property
    def data_(self):
        return self.dropdown.value, self.textfield.value


class AddProductRow(ft.Row):
    def __init__(self, product: FakeProduct, column: ft.Column):
        super().__init__()
        self.product = product
        self.column = column
        self.expand = 1

        self.controls = [
            ft.Container(
                expand=3,
                blur=ft.Blur(10, 15, tile_mode=ft.BlurTileMode.CLAMP),
                alignment=ft.alignment.top_left,
                content=ft.Text(f'{self.product.name}', size=18, color=ft.colors.WHITE),
            ),
            ft.IconButton(icon=ft.icons.ADD, expand=1, icon_color=ft.colors.WHITE, bgcolor=ft.Colors.BLUE,
                          on_click=self.on_click),
        ]

    def on_click(self, _: ft.ControlEvent):
        self.column.controls.append(ProductRow(self.product))
        self.column.update()

    @property
    def data_(self):
        return self.product


class AllProducts(ft.Column):
    def __init__(self, products: list[FakeProduct], column: ft.Column):
        super().__init__()
        self.expand = 8
        self.scroll = ft.ScrollMode.ALWAYS
        list_products = [
            AddProductRow(product, column) for product in products
        ]
        self.controls = list_products


class ProductRow(ft.Row):
    def __init__(self, product: FakeProduct):
        super().__init__()
        self.parent: ft.Column
        self.product = product
        self.expand = 1
        self.count_field = ft.TextField(hint_text='Кол-во', expand=2, text_size=18)
        self.controls = [
            ft.Container(
                expand=1,
                blur=ft.Blur(10, 15, tile_mode=ft.BlurTileMode.CLAMP),
                alignment=ft.alignment.top_left,
                content=ft.Text(
                    value=f'{self.product.name}',
                    size=18,
                    color=ft.colors.WHITE,
                )
            ),
            ft.Container(
                expand=1
            ),
            ft.Container(
                expand=1,
                blur=ft.Blur(10, 15, tile_mode=ft.BlurTileMode.CLAMP),
                alignment=ft.alignment.top_left,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        self.count_field,
                        ft.IconButton(icon=ft.icons.DELETE, expand=1,
                                      on_click=self.delete_row)
                    ]
                )
            )
        ]

    @property
    def data_(self):
        return self.product, self.count_field.value

    def delete_row(self, _: ft.ControlEvent):
        self.parent.controls.remove(self)
        self.parent.update()


class ProductsContainer(ft.Container):
    def __init__(self):
        super().__init__()
        self.expand = 7
        self.border = ft.border.all(0)
        self.alignment = ft.alignment.top_left
        self.column = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True, controls=[])
        self.all_products = [AddProductRow(product, self.column) for product in fake_products]
        self.products_row = AllProducts(fake_products, self.column)
        self.filter = FilterRow(self.change_filter)
        self.column_all_products = ft.Column(
            controls=[
                self.filter,
                self.products_row
            ]
        )
        self.content = ft.Row(
            controls=[self.column,
                      ft.Container(
                          expand=1,
                          content=self.column_all_products
                      )]

        )

    def change_filter(self, _: ft.ControlEvent):
        category_filter, text_filter = self.filter.data_
        print(category_filter, text_filter)
        new_products = self.all_products.copy()
        print(new_products[0].data_)
        if int(category_filter):
            new_products = [product for product in new_products if
                            product.data_.category[0].id == int(category_filter)]
        if text_filter:
            new_products = [product for product in new_products if
                            text_filter.lower() in product.data_.name.lower()]
        self.products_row.controls = new_products
        self.products_row.update()


class TabDesc(ft.Tab):
    def __init__(self, tabs: 'TabsDesc', **kwargs):
        super().__init__(**kwargs)
        self.text = len(tabs.tabs) - 1 if len(tabs.tabs) else 1
        self.textfield = ft.TextField(multiline=True,
                                      expand=True,
                                      min_lines=5,
                                      border=InputBorder.NONE,
                                      text_vertical_align=-1.0,
                                      text_style=ft.TextStyle(
                                          italic=True,
                                          weight=ft.FontWeight.W_500,
                                          size=18,
                                          color=ft.colors.WHITE
                                      ),
                                      label=f'{self.text}. Этап',
                                      prefix_text=f'{self.text}. ',
                                      align_label_with_hint=True,
                                      label_style=ft.TextStyle(
                                          italic=True,
                                          size=20,
                                          color=ft.colors.WHITE
                                      ),
                                      prefix_style=ft.TextStyle(
                                          italic=True,
                                          size=18,
                                          color=ft.colors.WHITE
                                      ))
        self.content: ft.Container = ft.Container(
            expand=1,
            blur=ft.Blur(10, 15, tile_mode=ft.BlurTileMode.CLAMP),
            alignment=ft.alignment.top_left,
            content=self.textfield
        )

    @property
    def data_(self):
        return self.textfield.value


class TabsDesc(ft.Tabs):
    tab_add = ft.Tab(icon=ft.Icons.ADD)
    tab_minus = ft.Tab(icon=ft.Icons.REMOVE)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.expand = 5
        self.on_change = self.new_tab
        self.tabs: list[TabDesc] = [
            TabDesc(self),
            self.tab_add,
            self.tab_minus
        ]

    def new_tab(self, _):
        if self.selected_index == len(self.tabs) - 2:
            self.tabs[-2] = TabDesc(self)
            self.tabs[-1] = self.tab_add
            self.tabs.append(self.tab_minus)
            self.update()
            for tab in self.tabs:
                tab.update()
                if tab.content:
                    tab.content.update()
            self.selected_index = len(self.tabs) - 3
            self.update()
        elif self.selected_index == len(self.tabs) - 1:
            if len(self.tabs) == 3:
                self.selected_index = 0
                self.update()
                return
            self.tabs.pop()
            self.tabs[-2] = self.tab_add
            self.tabs[-1] = self.tab_minus
            self.update()

    @property
    def data_(self):
        return [tab.data_ for tab in self.tabs if tab if isinstance(tab, TabDesc)]


class AddRecipe(MainApp):
    def __init__(self):
        self.my_tabs = None

    def view(self, page: ft.Page, params: Params, basket: Basket):
        MainApp.view(self, page, params, basket)
        container = self.controls[-1]
        container.image = ft.DecorationImage(
            src="images/add_recipe_background.webp", repeat=ft.ImageRepeat.REPEAT
        )

        self.my_tabs = TabsDesc()

        container.content = ft.Column(
            controls=[row_high,
                      self.my_tabs,
                      ProductsContainer(),
                      row_add]
        )

        def func(e):
            if e.key == 'Q':
                print(self.my_tabs.data_)

        page.on_keyboard_event = func
        return self.main_view
