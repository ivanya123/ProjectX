import flet as ft
from flet.core.border import BorderSide
from flet_route import Params, Basket

from app.pages.mainapp import MainApp
from app.styles import *
from database import *


def type_to_suffix(product_type: str):
    if product_type == 'штучный':
        return 'шт.'
    elif product_type == 'весовой':
        return 'г.'
    elif product_type == 'жидкий':
        return 'мл.'


def validate_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


class ProductRow(ft.Row):
    def __init__(self, fridge_row: Fridge):
        super().__init__()
        self.fridge_row = fridge_row
        self.type = self.fridge_row.products.product_type

        self.vertical_alignment = ft.CrossAxisAlignment.START
        self.spacing = 5
        self.height = 40
        self.expand = True
        self.padding = ft.padding.only(left=10, right=10)

        self.text_name = ft.Text(
            self.fridge_row.products.name,
            style=MAIN_STYLE_TEXT,
            expand=3
        )
        self.slider = ft.Slider(
            min=0,
            max=30 if self.type == 'штучный' else 3000,
            value=self.fridge_row.amount,
            on_change=self.slider_change,
            expand=10
        )
        self.slider.divisions = self.slider.max
        self.text_amount = ft.TextField(
            value=f"{self.fridge_row.amount:.0f}", text_align=ft.TextAlign.RIGHT,
            on_change=self.text_amount_change,
            text_style=MAIN_STYLE_TEXT,
            suffix_text=type_to_suffix(self.type),
            suffix_style=MAIN_STYLE_TEXT,
            expand=2
        )
        self.add_icon = ft.IconButton(
            expand=1,
            icon=ft.icons.ADD,
            icon_color=ft.Colors.ORANGE_200,
            on_click=self.add_amount,
        )
        self.remove_icon = ft.IconButton(
            expand=1,
            icon=ft.icons.REMOVE,
            icon_color=ft.Colors.ORANGE_200,
            on_click=self.remove_amount
        )

        self.delta_amount = 1 if self.type == 'штучный' else 50

        self.controls = [
            ft.Container(
                expand=3,
                alignment=ft.alignment.center_left,
                blur=ft.Blur(10, 15, tile_mode=ft.BlurTileMode.CLAMP),
                content=self.text_name
            ),
            self.slider,
            self.add_icon,
            self.text_amount,
            self.remove_icon
        ]

    def slider_change(self, e):
        self.text_amount.value = f"{e.control.value:.0f}"
        self.text_amount.update()

    def text_amount_change(self, e):
        if validate_number(e.control.value):
            self.slider.value = float(e.control.value)
            self.slider.update()

    def add_amount(self, _):
        self.slider.value += self.delta_amount
        self.text_amount.value = f"{self.slider.value:.0f}"
        self.text_amount.update()
        self.slider.update()

    def remove_amount(self, _):
        self.slider.value -= self.delta_amount
        self.text_amount.value = f"{self.slider.value:.0f}"
        self.text_amount.update()
        self.slider.update()


class FilterProductsRow(ft.Container):
    def __init__(self, all_fridge: 'FridgeHome'):
        super().__init__()
        self.expand = 1
        self.all_fridge = all_fridge
        self.blur = ft.Blur(10, 15, tile_mode=ft.BlurTileMode.CLAMP)
        self.text_filter = ft.TextField(hint_text='Фильтр по названию', hint_style=HINT_STYLE_TEXT,
                                        text_style=MAIN_STYLE_TEXT, expand=2, on_change=self.filter)
        self.list_checkbox = [ft.Checkbox(label=f'{category.name}', value=False, on_change=self.filter) for
                              category in reading_categories()]
        self.text_categories = ft.Text(value='Категории: ', style=MAIN_STYLE_TEXT, expand=3)
        self.content = ft.Row(
            controls=[
                self.text_filter,
                self.text_categories,
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(
                            content=ft.Column(
                                controls=self.list_checkbox
                            )
                        )
                    ]
                )
            ]
        )

    @property
    def data_filter(self):
        return {
            'category': [checkbox.label for checkbox in self.list_checkbox if checkbox.value],
            'name': self.text_filter.value.strip()
        }

    def filter(self, e: ft.ControlEvent):
        control = e.control
        if isinstance(control, ft.Checkbox):
            self.text_categories.value = f"Категории: {', '.join(checkbox.label for checkbox
                                                                 in self.list_checkbox if checkbox.value)}"
        self.update()
        self.all_fridge.filter(self.data_filter)


class FridgeHome(ft.Container):
    def __init__(self, all_fridge_rows: list[Fridge]):
        super().__init__()
        self.all_fridge_rows = all_fridge_rows
        self.expand = True
        self.height = 800
        self.border = ft.border.all(3, ft.colors.ORANGE_200)
        self.border_radius = 10
        self.padding = ft.padding.only(left=5, right=5, top=10, bottom=10)
        self.list_product_row = [
            ft.Container(
                expand=True,
                height=50,
                content=ProductRow(fridge_row),
                border=ft.border.only(bottom=BorderSide(3, color=ft.Colors.ORANGE_200)),

            ) for fridge_row in all_fridge_rows
        ]
        self.content = ft.Column(
            scroll=ft.ScrollMode.ALWAYS,
            expand=True,
            controls=self.list_product_row
        )

    def filter(self, data_filter: dict):
        filter_products = [fridge for fridge in self.all_fridge_rows]

        if data_filter['name']:
            filter_products = [p for p in filter_products if data_filter['name'].lower() in p.products.name.lower()]

        if data_filter['category']:
            category_set = set(data_filter['category'])
            filter_products = [p for p in filter_products if
                               category_set.intersection({cat.name for cat in p.products.category_list})]

        self.content.controls = [ProductRow(p) for p in filter_products]
        self.content.update()


# TODO: удалить после того как будет реализована логика базы данных.
list_fridge = [Fridge(
    id=i,
    products=product,
    amount=5.0
) for i, product in enumerate(reading_products()) if i % 2 == 0]


class BottomSheetAddProduct(ft.BottomSheet):
    def __init__(self, fridge_home: FridgeHome, list_products: list[Products]):
        super().__init__(ft.Container())
        self.fridge_home = fridge_home
        self.shape = ft.ContinuousRectangleBorder(radius=10)
        self.content = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text(f'{prod.name}'),
                    on_click=lambda _, product=prod: self.on_click_prod(product),
                    ink=True,
                    ink_color=ft.colors.BLUE_300
                ) for prod in list_products
            ]
        )

    def on_click_prod(self, product: Products):
        self.fridge_home.content.controls.append(
            ProductRow(Fridge())
        )


class FridgePage(MainApp):
    def __init__(self):
        super().__init__()
        self.filter_products_row = None
        self.fridge_home = None

    def view(self, page: ft.Page, params: Params, basket: Basket):
        MainApp.view(self, page, params, basket)
        container = self.controls[-1]
        container.image = ft.DecorationImage(
            src="images/fridge_background.webp", repeat=ft.ImageRepeat.REPEAT
        )
        self.fridge_home = FridgeHome(list_fridge)
        self.filter_products_row = FilterProductsRow(self.fridge_home)
        container.content = ft.Column(
            controls=[
                self.filter_products_row,
                self.fridge_home
            ]
        )

        return self.main_view
