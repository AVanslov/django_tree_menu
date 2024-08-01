from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Menu, MenuItem


class MenuItemsInstanceInline(admin.TabularInline):
    model = MenuItem


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'display_menu_items'
    )
    inlines = [MenuItemsInstanceInline]

    @admin.display(description='Пункты', empty_value=None)
    def display_menu_items(self, menu):
        menu_items = MenuItem.objects.filter(menu__name=menu.name)

        def subitems_generator(menu_item, menu: str):
            """
            Проверяет, есть ли в переданном пункте меню дочерние пункты
            и возвращает часть html кода с подпунктами переданного пункта.
            """

            item = (
                '<li>'
                f'{menu_item.name}'
                '<ul>'
            )
            end_tag = '</ul>'

            menu += item
            menu += children_items(items=menu_item)
            menu += end_tag
            return menu

        def children_items(items):
            """
            Генерирует списки с подсписками
            до тех пор, пока есть дочерние пункты меню.
            """
            menu_item_code = str()
            for menu_item in items.children.all():
                menu_item_code = subitems_generator(
                    menu_item, menu=menu_item_code
                )
            return menu_item_code
        static = (
            """
            <style>
                .treeCSS,
                .treeCSS ul,
                .treeCSS li {
                margin: 0;
                padding: 0;
                line-height: 1;
                list-style: none;
                }
                .treeCSS ul {
                margin: 0 0 0 .5em;
                }
                .treeCSS > li:not(:only-child),
                .treeCSS li li {
                position: relative;
                padding: .2em 0 0 1.2em;
                }
                .treeCSS li:not(:last-child) {
                border-left: 1px solid #ccc;
                }
                .treeCSS li li:before,
                .treeCSS > li:not(:only-child):before {
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                width: 1.1em;
                height: .7em;
                border-bottom: 1px solid #ccc;
                }
                .treeCSS li:last-child:before {
                width: calc(1.1em - 1px);
                border-left: 1px solid #ccc;
                }

            </style>
            """
        )
        menu = static + '<ul class="treeCSS">'
        for menu_item in menu_items:
            # инициируем генерацию html кода меню
            if menu_item.level == 0:
                menu = subitems_generator(menu_item, menu=menu)

        menu += '</ul>'
        return mark_safe(menu)
        # return mark_safe(
        #     '<br>'.join(
        #         [
        #             str(
        #                 get_object_or_404(
        #                     MenuItem,
        #                     menu=menu,
        #                     id=menu_item.id,
        #                 ).name
        #             )
        #             for menu_item in menu.menuitems.all()
        #         ]
        #     )
        # )
