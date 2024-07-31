from django.contrib import admin
from django.shortcuts import get_object_or_404
from django.utils.safestring import mark_safe

from .models import Menu, MenuItem

# admin.site.register(Page)


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
        return mark_safe(
            '<br>'.join(
                [
                    str(
                        get_object_or_404(
                            MenuItem,
                            menu=menu,
                            id=menu_item.id,
                        ).name
                    )
                    for menu_item in menu.menuitems.all()
                ]
            )
        )
