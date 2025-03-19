import flet as ft
from flet.core.border import BorderSide
from flet_route import Params, Basket

from app.pages.mainapp import MainApp
from app.styles import *
from database import *
from app.utils import type_to_suffix

def validate_number(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


def max_slider_value(product_type: str):
    if product_type == 'штучный':
        return 30
    elif product_type == 'весовой':
        return 3000
    elif product_type == 'жидкость':
        return 3000


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
        self.MAX_SLIDER_VALUE = max_slider_value(self.type)

        self.text_name = ft.Text(
            self.fridge_row.products.name,
            style=MAIN_STYLE_TEXT,
            expand=3
        )
        self.slider = ft.Slider(
            min=0,
            max=self.MAX_SLIDER_VALUE if self.MAX_SLIDER_VALUE > self.fridge_row.amount else self.fridge_row.amount + 1,
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
            icon_color=ft.Colors.BLUE_200,
            on_click=self.add_amount,
            bgcolor=ft.colors.ORANGE_200
        )
        self.remove_icon = ft.IconButton(
            expand=1,
            icon=ft.icons.REMOVE,
            icon_color=ft.Colors.BLUE_200,
            on_click=self.remove_amount,
            bgcolor=ft.colors.ORANGE_200
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
            self.remove_icon,
            ft.Container(
                expand=3,
                alignment=ft.alignment.center_left,
                blur=ft.Blur(10, 15, tile_mode=ft.BlurTileMode.CLAMP),
                content=self.text_amount
            ),
            self.add_icon,
        ]

    def slider_change(self, e):

        self.text_amount.value = f"{e.control.value:.0f}"
        self.fridge_row.amount = self.slider.value
        changing_fridge(self.fridge_row)
        self.text_amount.update()

    def text_amount_change(self, e):
        if validate_number(e.control.value):
            if self.slider.max >= float(e.control.value) >= 0:
                self.slider.value = float(e.control.value)
                self.fridge_row.amount = self.slider.value

            elif float(e.control.value) >= self.slider.max:
                self.slider.max = int(e.control.value) + 1
                self.slider.value = int(e.control.value)

            elif self.MAX_SLIDER_VALUE <= int(e.control.value) <= self.slider.max:
                self.slider.value = int(e.control.value)
                self.slider.max = int(e.control.value) + 1

            else:
                self.page.open(DeleteDialog(self))
            if int(e.control.value) <= self.MAX_SLIDER_VALUE:
                self.slider.max = self.MAX_SLIDER_VALUE
            self.fridge_row.amount = self.slider.value
            changing_fridge(self.fridge_row)
            self.slider.update()

    def add_amount(self, _):
        if self.slider.value + self.delta_amount >= self.MAX_SLIDER_VALUE:
            self.slider.max = self.slider.value + self.delta_amount + 1

        self.slider.value += self.delta_amount
        self.text_amount.value = f"{self.slider.value:.0f}"
        self.text_amount.update()
        self.slider.update()
        self.fridge_row.amount = self.slider.value
        changing_fridge(self.fridge_row)

    def remove_amount(self, _):
        if self.slider.max > self.MAX_SLIDER_VALUE:
            self.slider.max -= self.delta_amount

        if self.slider.value - self.delta_amount > 0:
            self.slider.value -= self.delta_amount
            self.text_amount.value = f"{self.slider.value:.0f}"
            self.text_amount.update()
            self.slider.update()
            self.fridge_row.amount = self.slider.value
            changing_fridge(self.fridge_row)
        else:
            self.page.open(DeleteDialog(self))


class DeleteDialog(ft.AlertDialog):
    def __init__(self, row: ProductRow):
        super().__init__()
        self.modal = True
        self.row = row
        self.title = ft.Text('Удаление продукта из холодильника', style=MAIN_STYLE_TEXT)
        self.content = ft.Text('Вы действительно хотите удалить продукт из холодильника?', style=MAIN_STYLE_TEXT)
        self.actions = [
            ft.TextButton('Удалить', on_click=self.delete),
            ft.TextButton('Отмена', on_click=self.cancel)
        ]

    def delete(self, _):
        deleteing_fridge(self.row.fridge_row.id)
        self.page.close(self)
        self.row.parent.parent.controls.remove(self.row.parent)
        self.row.parent.parent.update()

    def cancel(self, _):
        self.page.update()
        self.page.close(self)


class FilterProductsRow(ft.Container):
    def __init__(self, all_fridge: 'FridgeHome'):
        super().__init__()
        self.expand = 1
        self.all_fridge = all_fridge
        self.blur = ft.Blur(10, 15, tile_mode=ft.BlurTileMode.CLAMP)
        self.text_filter = ft.TextField(hint_text='Фильтр по названию', hint_style=HINT_STYLE_TEXT,
                                        text_style=MAIN_STYLE_TEXT, expand=2, on_change=self.filter)
        self.list_checkbox = [ft.Checkbox(label=f'{category.name}',
                                          label_style=MAIN_STYLE_TEXT,
                                          value=False,
                                          on_change=self.filter) for
                              category in reading_categories()]
        self.text_categories = ft.Text(value='Категории: ', style=MAIN_STYLE_TEXT, expand=3)

        self.add_products_button = ft.TextButton(
            text='Добавить продукт',
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5),
                                 text_style=MAIN_STYLE_TEXT, color=ft.colors.WHITE),
            icon=ft.icons.ADD,
            icon_color=ft.colors.ORANGE_200,
            on_click=self.add_product
        )
        self.content = ft.Row(
            controls=[
                self.text_filter,
                self.add_products_button,
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

    def add_product(self, _):
        sheet = BottomSheetAddProduct(self.all_fridge, reading_products())
        self.page.open(sheet)

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
                key=fridge_row.id,
                content=ProductRow(fridge_row),
                border=ft.border.only(bottom=BorderSide(3, color=ft.Colors.ORANGE_200)),

            ) for fridge_row in self.all_fridge_rows
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


class BottomSheetAddProduct(ft.BottomSheet):
    def __init__(self, fridge_home: FridgeHome, list_products: list[Products]):
        super().__init__(ft.Container())
        self.fridge_home = fridge_home
        self.shape = ft.ContinuousRectangleBorder(radius=10)
        self.content = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text(f'{prod.name}', style=MAIN_STYLE_TEXT),
                    on_click=lambda _, product=prod: self.on_click_prod(_, product),
                    ink=True,
                    ink_color=ft.colors.BLUE_300
                ) for prod in list_products
            ]
        )

    def on_click_prod(self, _, product: Products):
        products_in_fridge = [cont.content.fridge_row.products.name for cont in self.fridge_home.content.controls]
        new_fridge_row = Fridge(
            products=product,
            amount=1.0
        )
        if product.name not in products_in_fridge:
            new_id = add_in_fridge(new_fridge_row)
            new_fridge_row.id = new_id
            new_row = ProductRow(new_fridge_row)
            new_container = ft.Container(
                expand=True,
                height=50,
                key=new_id,  # Указываем ключ
                content=new_row,
                border=ft.border.only(bottom=BorderSide(3, color=ft.Colors.ORANGE_200)),
            )
            self.fridge_home.content.controls.append(new_container)
            self.fridge_home.content.update()
            self.page.close(self)
            self.page.update()
            self.fridge_home.content.scroll_to(key=new_id, duration=1000)
            new_row.text_amount.focus()
            self.fridge_home.content.update()
        else:
            new_row = None
            for row in self.fridge_home.content.controls:
                cont = row.content
                if cont.fridge_row.products.name == product.name:
                    new_row = cont
                    new_id = cont.fridge_row.id
                    break
            else:
                new_id = 1
            self.page.close(self)
            self.page.update()
            self.fridge_home.content.scroll_to(key=new_id, duration=1000)
            new_row.text_amount.focus()
            self.fridge_home.content.update()


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
        self.fridge_home = FridgeHome(self.all_fridge)
        self.filter_products_row = FilterProductsRow(self.fridge_home)
        container.content = ft.Column(
            controls=[
                self.filter_products_row,
                self.fridge_home
            ]
        )

        return self.main_view
