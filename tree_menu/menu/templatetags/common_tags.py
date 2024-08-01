from django import template
from django.utils.safestring import mark_safe
from menu.models import MenuItem

register = template.Library()


@register.inclusion_tag('templatetags/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    menu_items = MenuItem.objects.filter(menu__name=menu_name)

    def subitems_generator(menu_item, menu: str):
        """
        Проверяет, есть ли в переданном пункте меню дочерние пункты
        и возвращает часть html кода с подпунктами переданного пункта.
        """
        details = '<details>'
        link_class = 'btn btn-primary'
        current_url = context.request.path
        # если в текущем пути есть адрес текущей страницы
        if menu_item.url in current_url:
            details = '<details open>'
            link_class = 'btn btn-primary active'
        # если есть подпункты
        if menu_item.children.all():
            # если в одном из дочерних путей есть адрес текущей страницы
            if any(
                child.url in current_url
                for child in menu_item.children.all()
            ):
                details = '<details open>'
                link_class = 'btn btn-primary'

            item = (
                '<div class="m-1">'
                f'<a class="{link_class}" '
                f'role="button" href="http://127.0.0.1:8000/{menu_item.url}">'
                f'{menu_item.name}</a>'
                + details
                + '<summary></summary>'
            )
            end_tag = '</details></div>'
        # если нет подпунктов
        else:
            item = (
                f'<div class="m-1"><a class="{link_class}" '
                f'role="button" href="http://127.0.0.1:8000/{menu_item.url}">'
                f'{menu_item.name}</a>'
            )
            end_tag = '</div>'

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
            menu_item_code = subitems_generator(menu_item, menu=menu_item_code)
        return menu_item_code

    menu = '<div class="treeHTML">'
    for menu_item in menu_items:
        # инициируем генерацию html кода меню
        if menu_item.level == 0:
            menu = subitems_generator(menu_item, menu=menu)

    menu += '</div>'

    return {
        "menu_items": menu_items,
        "menu": mark_safe(menu)
        # "menu": menu
    }
