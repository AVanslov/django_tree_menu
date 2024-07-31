from django.db import models
from django.db.models import UniqueConstraint
from django.shortcuts import get_object_or_404
from django.urls import reverse


class Menu(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'


# class Page(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#     url = models.URLField('Ссылка', max_length=500)

#     def __str__(self):
#         return f'{str(self.name)}, {str(self.url)}'

#     class Meta:
#         verbose_name = 'Страница'
#         verbose_name_plural = 'Страницы'


class MenuItem(models.Model):
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name='menuitems'
    )
    name = models.CharField('Наименование', max_length=500, unique=True)
    # page = models.ForeignKey(
    #     Page,
    #     on_delete=models.CASCADE,
    #     null=True,
    #     blank=True,
    #     # related_name='menuitems'
    # )
    slug = models.SlugField('Слаг', max_length=100)
    # url = models.CharField('Ссылка', max_length=255)
    position = models.PositiveIntegerField('Позиция', default=1)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    def __str__(self):
        return str(self.name)

    @property
    def url(self):
        def has_parent(item, url=''):
            print(item.parent)
            if item.parent:
                url += item.parent.slug + '/' + item.slug + '/'
                # if item.parent.parent:
                has_parent(item=item.parent, url=url)
            else:
                url = item.slug + '/' + url
            return url
        return has_parent(self)

    @property
    def level(self):
        """
        Записывает уровень текущего элемента
        в иерархии данной модели.
        """
        def has_parent(item, level=0):
            if item.parent:
                level += 1
                level = has_parent(item=item.parent, level=level)
            return level

        return has_parent(self)

    # def get_absolute_url(self):
    #     return reverse('menu_item_page', kwargs={"pk": self.pk})

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['menu', 'name'], name='unique_menu_item'
            ),
        ]
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'
        ordering = ('position',)


# можно создавать неограниченое количество меню
# в каждом меню есть какие то поля
# у всех полей есть родительские поля
# у главного родителя родителя нет
# 