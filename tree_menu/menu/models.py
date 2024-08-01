from django.db import models
from django.db.models import UniqueConstraint


class Menu(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'


class MenuItem(models.Model):
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name='menuitems'
    )
    name = models.CharField('Наименование', max_length=500, unique=True)
    slug = models.SlugField('Слаг', max_length=100)
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
            if item.parent is None:
                url = item.slug + '/' + url
            else:
                url = item.slug + '/' + url
                url = has_parent(item=item.parent, url=url)
            return url
        return has_parent(item=self)

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

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['menu', 'name'], name='unique_menu_item'
            ),
        ]
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'
        ordering = ('position',)
