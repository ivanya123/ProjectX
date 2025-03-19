import flet as ft
from flet.core.form_field_control import InputBorder
from flet_route import Params, Basket

from app.pages.mainapp import MainApp
from app.styles import *
from app.utils import *
from database import *



class ColumnRecipes(ft.Column):
    def __init__(self, list_recipes: list[Recipes], show_edit_recipe: callable):
        super().__init__()
        self.expand = 1
        self.list_recipes = list_recipes
        self.scroll = ft.ScrollMode.ALWAYS
        self.controls = [
            ft.Container(
                alignment=ft.alignment.center_left,
                height=45,
                border=ft.border.all(2, ft.Colors.BLUE_50),
                border_radius=ft.border_radius.all(5),
                margin=ft.margin.only(top=5),
                data=recipe,
                on_click=lambda e, recipes=recipe: show_edit_recipe(e, recipes),
                content=ft.Text(recipe.name, style=MAIN_STYLE_TEXT),
                ink=True,
                ink_color='#b3a696'
            ) for recipe in list_recipes
        ]


class BottomSheetRecipes(ft.BottomSheet):
    def __init__(self, list_recipes: list[Recipes], show_edit_recipe: callable):
        super().__init__(ft.Container())
        self.maintain_bottom_view_insets_padding = True
        self.size_constraints = ft.BoxConstraints(min_width=500)
        self.list_recipes = list_recipes
        self.show_edit_recipe = show_edit_recipe

        self.elevation = 10.0
        self.shape = ft.ContinuousRectangleBorder(radius=10)
        self.content = ColumnRecipes(reading_recipes(), self.show_edit_recipe)


class ContainerAddEditRecipe(ft.Container):
    def __init__(self, name_field: ft.TextField, desc_tabs: 'TabsDesc', products_container: 'ProductsContainer',
                 list_recipes: list[Recipes]):
        super().__init__()
        self.bottom_sheet = None
        self.recipe = None
        self.list_recipes = list_recipes
        self.data = None
        self.name_field = name_field
        self.desc_tabs = desc_tabs
        self.products_container = products_container
        self.expand = 1
        self.add_container = ft.Container(
            blur=ft.Blur(1, 50, tile_mode=ft.BlurTileMode.MIRROR),
            content=ft.Text("Добавить рецепт", style=MAIN_STYLE_TEXT),
            on_click=lambda _: self.add_recipe(),
            ink=True,
            ink_color='#b3a696'
        )
        self.edit_container = ft.Container(
            blur=ft.Blur(1, 50, tile_mode=ft.BlurTileMode.MIRROR),
            content=ft.Text("Редактировать рецепт", style=MAIN_STYLE_TEXT),
            on_click=lambda _: self.edit_recipe_container(),
            ink=True,
            ink_color='#b3a696'
        )
        self.clear_container = ft.Container(
            blur=ft.Blur(1, 50, tile_mode=ft.BlurTileMode.MIRROR),
            content=ft.Text("Очистить форму", style=MAIN_STYLE_TEXT),
            on_click=lambda _: self.clear_form(),
            ink=True,
            ink_color='#b3a696'
        )
        self.content = ft.Row(
            alignment=ft.MainAxisAlignment.START,
            controls=[
                self.add_container,
                self.edit_container,
                self.clear_container
            ]
        )

    def show_alert(self, message: str):
        alert_dialog = ft.AlertDialog(
            title=ft.Text(message),
            on_dismiss=None,
        )

        self.page.open(alert_dialog)

    def valid_form(self, name: str, desc: str, list_products: list[Products]) -> bool:
        if not name:
            self.show_alert("Введите название рецепта")
            return False
        if not desc.strip():
            self.show_alert("Некорректно введены этапы приготовления")
            return False
        if not list_products:
            self.show_alert("Добавьте продукты в список")
            return False
        return True

    def add_recipe(self):
        name = self.name_field.value.strip()
        desc = create_description(self.desc_tabs.data_)
        list_products = self.products_container.data_
        if self.valid_form(name=name, desc=desc, list_products=list_products):
            new_recipe = Recipes(
                name=name,
                description=desc,
                product_list=list_products
            )
            add_in_recipes(new_recipe)
            self.clear_form()

    def edit_recipe_container(self):
        self.bottom_sheet = BottomSheetRecipes(self.list_recipes, self.show_edit_recipe)
        self.page.open(self.bottom_sheet)

    def clear_form(self):
        self.recipe = None
        self.add_container.on_click = lambda _: self.add_recipe()
        self.add_container.content = ft.Text("Добавить рецепт", style=MAIN_STYLE_TEXT)
        self.name_field.value = ''
        self.desc_tabs.clear()
        self.products_container.clear()
        self.page.update()

    def show_edit_recipe(self, _, recipe: Recipes):
        self.recipe = recipe
        self.name_field.value = self.recipe.name
        self.desc_tabs.show_edit_recipe(self.recipe.description)
        self.products_container.column_recipes.controls = [ProductRow(product) for product in self.recipe.product_list]
        self.add_container.on_click = self.edit_recipe
        self.add_container.content = ft.Text("Подтвердить изменения", style=MAIN_STYLE_TEXT)
        self.page.close(self.bottom_sheet)
        self.page.update()

    def edit_recipe(self, _):
        new_recipe = Recipes(
            id=self.recipe.id,
            name=self.name_field.value,
            description=create_description(self.desc_tabs.data_),
            product_list=self.products_container.data_
        )
        changing_del_recipes(new_recipe)
        self.clear_form()


container_name = ft.Container(expand=2,
                              content=ft.TextField(hint_text='Введите название рецепта',
                                                   hint_style=MAIN_STYLE_TEXT,
                                                   label='Название рецепта',
                                                   label_style=LABEL_STYLE_TEXT,
                                                   text_style=MAIN_STYLE_TEXT,
                                                   border=InputBorder.NONE,
                                                   multiline=True,
                                                   max_lines=2),
                              blur=ft.Blur(1, 50, tile_mode=ft.BlurTileMode.CLAMP),
                              alignment=ft.alignment.top_right,
                              border=ft.border.all(1, '#b3a696'),
                              border_radius=5)


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


class AddProductRow(ft.Row):
    def __init__(self, product: Products, column: ft.Column):
        super().__init__()
        self.product = product
        self.column = column
        self.expand = 1
        self.text_ = ft.Text(f'{self.product.name}', style=MAIN_STYLE_TEXT)
        self.controls = [
            ft.Container(
                expand=4,
                blur=ft.Blur(10, 15, tile_mode=ft.BlurTileMode.CLAMP),
                alignment=ft.alignment.top_left,
                content=self.text_,
                height=self.text_.style.size * 1.2,
            ),
            ft.IconButton(icon=ft.icons.ADD, expand=1, icon_color=ft.colors.WHITE, bgcolor=ft.Colors.BLUE,
                          on_click=self.on_click, tooltip='Добавить', height=self.text_.style.size * 1.2, padding=0)
        ]

    def on_click(self, _: ft.ControlEvent):
        self.column.controls.append(ProductRow(self.product))
        self.column.update()

    @property
    def data_(self):
        return self.product


class AllProducts(ft.Column):
    def __init__(self, products: list[Products], column: ft.Column):
        super().__init__()
        self.products = products
        self.column_recipes = column
        self.expand = 8
        self.scroll = ft.ScrollMode.ALWAYS
        self.spacing = 3
        list_products = [
            AddProductRow(product, column) for product in products
        ]
        self.controls = list_products

    def filter(self, data_filter: dict):
        filter_products = [p for p in self.products]

        if data_filter['name']:
            filter_products = [p for p in filter_products if data_filter['name'].lower() in p.name.lower()]

        if data_filter['category']:
            category_set = set(data_filter['category'])
            filter_products = [p for p in filter_products if
                               category_set.intersection({cat.name for cat in p.category_list})]

        self.controls = [AddProductRow(p, self.column_recipes) for p in filter_products]
        self.update()


class ProductRow(ft.Row):
    def __init__(self, product: Products | tuple[Products, float]):
        super().__init__()
        self.parent: ft.Column
        self.product = product if isinstance(product, Products) else product[0]
        self.expand = 1
        self.container_product = ft.Container(
            expand=3,
            blur=ft.Blur(10, 15, tile_mode=ft.BlurTileMode.CLAMP),
            alignment=ft.alignment.top_left,
            content=ft.Text(
                value=f'{self.product.name}' if isinstance(self.product, Products) else f'{self.product[0].name}',
                style=MAIN_STYLE_TEXT
            )
        )

        self.count_field = ft.TextField(hint_text='Кол-во', content_padding=2,
                                        expand_loose=True, expand=2,
                                        hint_style=MAIN_STYLE_TEXT,
                                        text_style=MAIN_STYLE_TEXT)
        self.count_field.value = '' if isinstance(product, Products) else f"{product[1]}"

        self.controls = [
            self.container_product,
            ft.Container(
                expand=2,
                blur=ft.Blur(10, 15, tile_mode=ft.BlurTileMode.CLAMP),
                alignment=ft.alignment.top_left,
                height=self.count_field.text_style.size * 1.2,
                content=ft.Row(
                    expand=1,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        self.count_field,
                        ft.IconButton(icon=ft.icons.DELETE, expand=1,
                                      on_click=self.delete_row, icon_color=ft.colors.RED_ACCENT,
                                      hover_color=ft.colors.RED_50, tooltip='Удалить',
                                      icon_size=self.count_field.text_style.size,
                                      height=self.count_field.text_style.size * 1.2, padding=0)
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
    def __init__(self, products: list[Products]):
        super().__init__()
        self.expand = 7
        self.height = 300
        self.border = ft.border.all(0)
        self.alignment = ft.alignment.top_center
        self.column_recipes = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, controls=[],
                                        alignment=ft.MainAxisAlignment.START, spacing=3)
        self.all_products_container = AllProducts(products, self.column_recipes)
        self.filter_row = FilterProductsRow(self.all_products_container)
        self.column_all_products = ft.Column(
            controls=[
                self.filter_row,
                self.all_products_container
            ]
        )
        self.content = ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.START,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            spacing=1,
            controls=[self.column_recipes,
                      ft.Container(
                          expand=1,
                          content=self.column_all_products
                      )]

        )

    @property
    def data_(self) -> list[tuple[Products, float]]:
        try:
            products = [(row.data_[0], float(row.data_[1]))
                        for row in self.column_recipes.controls if isinstance(row, ProductRow)]
        except ValueError as e:
            self.show_alert(f"Введите числовые значения в поля 'кол-во' {e.args[0]}")
            return
        return products

    def clear(self):
        self.column_recipes.controls.clear()
        self.update()

    def show_alert(self, message: str):
        alert_dialog = ft.AlertDialog(
            title=ft.Text(message),
            on_dismiss=None,
        )

        self.page.open(alert_dialog)


class TabDesc(ft.Tab):
    def __init__(self, tabs: 'TabsDesc', clear=False, **kwargs):
        super().__init__(**kwargs)
        if not clear:
            self.text = len(tabs.tabs) - 1 if len(tabs.tabs) else 1
        else:
            self.text = 1
        self.text_style = TAB_STYLE_TEXT
        self.textfield = ft.TextField(multiline=True,
                                      expand=True,
                                      min_lines=5,
                                      border=InputBorder.NONE,
                                      text_vertical_align=-1.0,
                                      text_style=MAIN_STYLE_TEXT,
                                      label=f'{self.text}. Этап',
                                      label_style=LABEL_STYLE_TEXT,
                                      align_label_with_hint=True,
                                      prefix_text=f'{self.text}. ',
                                      prefix_style=MAIN_STYLE_TEXT)
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
        self.height = 250
        self.on_change = self.new_tab
        self.tabs: list[TabDesc] = [
            TabDesc(self),
            self.tab_add,
            self.tab_minus
        ]

    def new_tab(self, _):
        if self.selected_index == len(self.tabs) - 2:  # Добавление новой вкладки
            self.tabs.insert(-2, TabDesc(self))
            self.selected_index = len(self.tabs) - 3  # Выбираем новую вкладку
        elif self.selected_index == len(self.tabs) - 1:  # Удаление последней вкладки
            if len(self.tabs) > 3:
                self.tabs.pop(-3)
                self.selected_index = max(0, len(self.tabs) - 3)  # Переключаемся на последнюю доступную вкладку
            else:
                self.selected_index = 0  # Если осталась только 1 вкладка, выбираем её

        self.update()  # Однократное обновление UI

    @property
    def data_(self):
        return [tab.data_ for tab in self.tabs if tab if isinstance(tab, TabDesc)]

    def clear(self):
        self.tabs: list[TabDesc] = [
            TabDesc(self, clear=True),
            self.tab_add,
            self.tab_minus
        ]
        self.update()

    def show_edit_recipe(self, description):
        self.clear()
        list_desc = desc_to_list(description)

        self.selected_index = 2
        for i, desc in enumerate(list_desc):
            self.new_tab(None)
            if isinstance(self.tabs[-3], TabDesc):
                self.tabs[-3].textfield.value = desc  # ✅ Заполняем вкладку данными
                self.tabs[-3].update()  # ✅ Обновляем только изменённую вкладку
            self.selected_index += 1

        self.selected_index = 0
        self.update()  # ✅ Обновляем UI после всех изменений


class AddRecipe(MainApp):
    def __init__(self):
        super().__init__()
        self.name_field = None
        self.products_container = None
        self.add_row = None
        self.container_name = None
        self.my_tabs = None

    def view(self, page: ft.Page, params: Params, basket: Basket):
        MainApp.view(self, page, params, basket)
        container = self.controls[-1]
        container.image = ft.DecorationImage(
            src="images/add_recipe_background.webp", repeat=ft.ImageRepeat.REPEAT
        )
        self.name_field = ft.TextField(hint_text='Введите название рецепта',
                                       hint_style=MAIN_STYLE_TEXT,
                                       label='Название рецепта лучшего в мире',
                                       label_style=LABEL_STYLE_TEXT,
                                       text_style=MAIN_STYLE_TEXT,
                                       border=InputBorder.NONE,
                                       multiline=True,
                                       max_lines=2)
        self.container_name = ft.Container(expand=2,
                                           content=self.name_field,
                                           blur=ft.Blur(1, 50, tile_mode=ft.BlurTileMode.CLAMP),
                                           alignment=ft.alignment.top_right,
                                           border=ft.border.all(1, '#b3a696'),
                                           border_radius=5)
        self.my_tabs = TabsDesc()
        self.products_container = ProductsContainer(products=self.all_products)
        self.add_row = ContainerAddEditRecipe(self.name_field, self.my_tabs, self.products_container,
                                              self.all_recipes)

        container.content = ft.Column(
            controls=[self.container_name,
                      self.my_tabs,
                      self.products_container,
                      self.add_row]
        )

        def func(e):
            if e.key == 'Q':
                print(self.products_container.data_)

        page.on_keyboard_event = func

        return self.main_view
