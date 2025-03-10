from collections.abc import Callable

import flet as ft
from flet_route import Params, Basket

from app.pages.mainapp import MainApp
from app.styles import *
from database import *


class ContainerCategory(ft.Container):
    def __init__(self, category: Categories, func_category: Callable, long_press: Callable):
        super().__init__()
        self.category = category
        self.blur = ft.Blur(10, 15, tile_mode=ft.BlurTileMode.CLAMP)
        self.content = ft.Text(category.name, style=MAIN_STYLE_TEXT)
        self.on_click = func_category
        self.on_long_press = long_press
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
        self.text_ = ft.TextField(hint_text='Фильтр по названию', hint_style=HINT_STYLE_TEXT,
                                  text_style=MAIN_STYLE_TEXT, on_change=change)
        self.content = self.text_


class RadioType(ft.RadioGroup):
    def __init__(self, value: str = None):
        super().__init__(content=ft.Row())
        self.expand = 1
        self.content = ft.Column(
            spacing=0,
            alignment=ft.MainAxisAlignment.START,
            controls=[
                ft.Radio(value='весовой', label='Весовой', label_style=LABEL_STYLE_TEXT),
                ft.Radio(value='штучный', label='Штучный', label_style=LABEL_STYLE_TEXT),
                ft.Radio(value='жидкость', label='Жидкий', label_style=LABEL_STYLE_TEXT)
            ]
        )
        self.value = value


class ColumnAddProduct(ft.Column):
    def __init__(self, categories: list[Categories] = None, column_products: 'AllProducts' = None):
        super().__init__()
        self.categories = categories
        self.id_product = None
        self.border = ft.border.all(3, ft.colors.GREEN_900)
        self.expand = 3
        self.alignment = ft.MainAxisAlignment.SPACE_EVENLY
        self.radio_type = RadioType()
        self.in_category = ColumnCategory()
        self.all_category = ColumnCategory(
            categories_=([ContainerCategory(category, self.go_category, self.long_press_category)
                          for category in categories] if categories else []),
            right=True
        )
        self.text_name = ft.TextField(
            hint_text='Название продукта', hint_style=HINT_STYLE_TEXT,
            text_style=MAIN_STYLE_TEXT
        )
        self.controls = [
            ft.Container(
                expand=1,
                blur=ft.Blur(10, 15, tile_mode=ft.BlurTileMode.CLAMP),
                content=self.text_name,
            ),

            ft.Row(
                expand=5,
                controls=[
                    ft.Container(
                        expand=2,
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
                                ft.Text('Выбранные категории:', style=MAIN_STYLE_TEXT,
                                        bgcolor=ft.Colors.ORANGE_200),
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
                                ft.Text('Выберите категории:', style=MAIN_STYLE_TEXT,
                                        bgcolor=ft.Colors.ORANGE_200),
                                self.all_category
                            ]
                        )
                    )
                ]),
            ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.START,
                expand=1,
                controls=[
                    ft.IconButton(ft.Icons.ADD, on_click=lambda e: self.add_click(e, column_products)),
                    ft.IconButton(ft.Icons.CLEAR, on_click=self.clear_click)
                ]
            )

        ]

    def go_category(self, e: ft.ControlEvent):
        container_category: ContainerCategory = e.control
        parent: ColumnCategory = container_category.parent
        if parent.right:
            self.in_category.controls.append(ContainerCategory(container_category.category,
                                                               self.go_category,
                                                               self.long_press_category))
            self.all_category.controls.remove(container_category)
        elif not parent.right:
            self.all_category.controls.append(ContainerCategory(container_category.category,
                                                                self.go_category,
                                                                self.long_press_category))
            self.in_category.controls.remove(container_category)
        self.update()

    def add_click(self, _: ft.ControlEvent, column_products: 'AllProducts'):
        if self.valid_value():
            new_product: ProductView = Products(
                id=self.id_product,
                name=self.text_name.value,
                product_type=self.radio_type.value,
                category_list=[category.category for category in
                               self.in_category.controls] if self.in_category.controls else None
            )
            add_in_products(new_product)
            column_products.update_data(reading_products())
            column_products.update()
            self.clear_click(_)

    def valid_value(self):
        if not self.text_name.value.strip():
            self.alert('Введите название товара')
            return False
        if not self.radio_type.value:
            self.alert('Выберите тип товара')
            return False
        return True

    def alert(self, text: str):
        alert_dialog = ft.AlertDialog(
            title=ft.Text(text),
            on_dismiss=None,
        )
        self.page.open(alert_dialog)

    def clear_click(self, _: ft.ControlEvent):
        self.id_product = None
        self.text_name.value = ''
        self.in_category.controls.clear()
        self.all_category.controls = [ContainerCategory(category, self.go_category, self.long_press_category)
                                      for category in self.categories]
        self.radio_type.value = None

        self.parent.border = ft.border.all(4, ft.colors.ORANGE_200)
        self.parent.update()

    def edit_product(self, product: Products):
        self.id_product = product.id
        self.text_name.value = product.name
        self.radio_type.value = product.product_type
        self.in_category.controls = (
            [ContainerCategory(category, self.go_category, self.long_press_category) for category in
             product.category_list] if product.category_list else []
        )
        self.all_category.controls = (
            [ContainerCategory(category, self.go_category, self.long_press_category)
             for category in self.categories if category not in product.category_list] if product.category_list else [
                ContainerCategory(category, self.go_category, self.long_press_category) for category in self.categories
            ]
        )
        self.radio_type.value = product.product_type

        self.parent.border = ft.border.all(3, ft.colors.BLUE_900)
        self.parent.update()

    def update_data(self, categories: list[Categories]):
        # Определяем новые и удаляемые категории
        new_categories = [category for category in categories if category not in self.categories]
        remove_categories = [category for category in self.categories if category not in categories]

        # Добавляем новые категории
        if new_categories:
            self.categories.extend(new_categories)
            self.all_category.controls.extend(
                ContainerCategory(category, self.go_category, self.long_press_category) for category in new_categories)

        # Удаляем лишние категории
        if remove_categories:
            self.categories = [category for category in self.categories if category not in remove_categories]
            self.all_category.controls = [control for control in self.all_category.controls if
                                          control.category not in remove_categories]

        self.update()

    def long_press_category(self, e: ft.ControlEvent):
        parent: ColumnCategory = e.control.parent
        if parent.right:
            id_category = e.control.category.id
            deleteing_categories(id_category)
            self.update_data(reading_categories())
            self.update()
        else:
            print('Нельзя удалить категорию из левой колонки')


class ProductRow(ft.Container):
    def __init__(self, product: Products, edit_click: Callable):
        super().__init__()
        self.product: Products = product
        self.expand = 1
        self.blur = ft.Blur(10, 15, tile_mode=ft.BlurTileMode.CLAMP)
        self.category_text = ', '.join(
            category.name for category in product.category_list) if product.category_list else 'Без категории'
        self.content = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(value=f'{product.id}: {product.name}', style=MAIN_STYLE_TEXT, expand=5),
                ft.Text(value=product.product_type, style=MAIN_STYLE_TEXT, expand=4),
                ft.Text(value=self.category_text, style=MAIN_STYLE_TEXT, expand=4),
                ft.TextButton(on_click=edit_click, icon=ft.icons.EDIT),
                ft.TextButton(on_click=self.delete_click, icon=ft.icons.DELETE, icon_color=ft.colors.RED_400)
            ]
        )

    def delete_click(self, _: ft.ControlEvent):
        deleteing_products(self.product.id)
        container_products: 'AllProducts' = self.parent.parent

        container_products.products = [p for p in container_products.products if p.id != self.product.id]
        container_products.content.controls = [c for c in container_products.content.controls if
                                               c.product.id != self.product.id]

        container_products.update()


class FilterProductsRow(ft.Container):
    def __init__(self, column_products: 'AllProducts'):
        super().__init__()
        self.expand = 1
        self.column_products = column_products
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
        self.column_products.filter(self.data_filter)


class AllProducts(ft.Container):
    def __init__(self, products: list[Products] = None, edit_click: Callable = None):
        super().__init__()
        self.edit_click = edit_click
        self.products = products
        self.expand = 6
        self.padding = 10
        self.blur = ft.Blur(10, 15, tile_mode=ft.BlurTileMode.CLAMP)
        self.content = ft.Column(
            scroll=ft.ScrollMode.ALWAYS,
            controls=[ProductRow(product, self.edit_click) for product in self.products] if self.products else []
        )

    def update_data(self, products: list[Products]):

        existing_products_set = {p.id for p in self.products}
        new_products = [p for p in products if p.id not in existing_products_set]

        new_products_set = {p.id for p in products}
        delete_products = [p for p in self.products if p.id not in new_products_set]

        if new_products:
            self.products.extend(new_products)
            self.content.controls.extend(ProductRow(p, self.edit_click) for p in new_products)

        if delete_products:
            self.products = [p for p in self.products if p.id in new_products_set]
            self.content.controls = [c for c in self.content.controls if c.product.id in new_products_set]

        self.update()

    def filter(self, data_filter: dict[str, list[str] | str]):

        filter_products = [p for p in self.products]

        if data_filter['name']:
            filter_products = [p for p in filter_products if data_filter['name'].lower() in p.name.lower()]

        if data_filter['category']:
            category_set = set(data_filter['category'])
            filter_products = [p for p in filter_products if
                               category_set.intersection({cat.name for cat in p.category_list})]

        self.content.controls = [ProductRow(p, self.edit_click) for p in filter_products]
        self.update()


class RowAddCategory(ft.Row):
    def __init__(self, column_add_product: ColumnAddProduct):
        super().__init__()
        self.expand = 1
        self.name_field = ft.TextField(hint_text='Название категории', hint_style=HINT_STYLE_TEXT,
                                       text_style=MAIN_STYLE_TEXT,
                                       expand=True)
        self.alignment = ft.MainAxisAlignment.START
        self.controls = [
            self.name_field,
            ft.TextButton(on_click=lambda _: self.add_click(_), icon=ft.icons.ADD,
                          height=MAIN_STYLE_TEXT.size, tooltip='Добавить категорию', text='Добавить категорию',
                          style=ft.ButtonStyle(text_style=MAIN_STYLE_TEXT,
                                               color=ft.Colors.WHITE,
                                               icon_color=ft.colors.WHITE,
                                               icon_size=MAIN_STYLE_TEXT.size,
                                               alignment=ft.alignment.top_left),
                          expand=True)
        ]
        self.column_add_product = column_add_product

    def add_click(self, _: ft.ControlEvent):
        if self.name_field.value.strip():
            new_category = Categories(name=self.name_field.value.strip())
            add_in_categories(new_category)
            self.column_add_product.update_data(reading_categories())
            self.name_field.value = ""
            self.update()
        else:
            self.show_alert("Введите название категории")

    def show_alert(self, message: str):
        alert_dialog = ft.AlertDialog(
            title=ft.Text(message),
            on_dismiss=None,
        )

        self.page.open(alert_dialog)


class ProductView(MainApp):
    def __init__(self):
        MainApp.__init__(self)
        self.filter_row = None
        self.all_products_row = None
        self.column_add_product: ColumnAddProduct = None

    def view(self, page: ft.Page, params: Params, basket: Basket):
        MainApp.view(self, page, params, basket)
        container = self.controls[-1]
        container.image = ft.DecorationImage(
            src="images/products_background.webp", repeat=ft.ImageRepeat.REPEAT
        )

        self.all_products_row = AllProducts(products=self.all_products, edit_click=self.edit_click)
        self.column_add_product = ColumnAddProduct(categories=self.all_categories,
                                                   column_products=self.all_products_row)
        self.filter_row = FilterProductsRow(self.all_products_row)

        container.content = ft.Column(
            spacing=0,
            controls=[
                self.filter_row,
                self.all_products_row,
                ft.Container(content=self.column_add_product, expand=6, border_radius=ft.border_radius.all(5),
                             border=ft.border.all(4, ft.colors.ORANGE_200)),
                ft.Container(expand=1, border_radius=ft.border_radius.all(4),
                             border=ft.border.all(4, ft.colors.ORANGE_200),
                             content=RowAddCategory(self.column_add_product))
            ]
        )

        return self.main_view

    def edit_click(self, e: ft.ControlEvent):
        container_product: ProductRow = e.control.parent.parent
        self.column_add_product.edit_product(container_product.product)
