# Django приложение с древовидным меню

![example event parameter](https://github.com/AVanslov/django_tree_menu/actions/workflows/main.yml/badge.svg?event=push)

## Стек технологий проекта
![Python](https://img.shields.io/badge/-Python-black?style=for-the-badge&logo=python)
![Django](https://img.shields.io/badge/-Django-black?style=for-the-badge&logo=Django)
![SQLite](https://img.shields.io/badge/-SQLite-black?style=for-the-badge&logo=SQLite)

## Возможности

- Модуль menu можно вставлять в любой сторонний проект для создания в нем древовидных меню.
- Меню поддерживает любую степень вложенности.
- Новое меню создается через админ панель.
- Вставить новое меню в html шаблон можно с помощью тега 
    ```
    {% draw_menu 'Country Menu' %}
    ```
    , где Country Menu - наименование меню, которое администратор сервиса задал в админ панели.
- При клике на пункт меню происходит переход по ссылке соответствующей данному пункту. При этом все родительские пункты, а также подпункты первого порядка развернуты.
- Активный пункт меню определяемя исходя из URL текущей страницы.

## Презентация
В админ панели на странице со списком объектов отрисовывается схема с отображением иерархии пунктов меню
![View of the demo-admin](readme_images/demo-admin.png)
Пункты и подпункты меню можно создать, назначить slug и родительский элемент непосредственно на странице объекта меню.
![View of the demo-admin-country-menu](readme_images/demo-admin-country-menu.png)
Url страниц, соответствующих пунктам меню генерируется в models.py с помощью @property на основе slug текущего и всех его родительских объектов.

![View of the demo-admin-country-menu](readme_images/demo-main-page-cars-uk.png)

Поэтому не нужно для каждого пункта меню прописывать url, достаточно указать slug. Возможно, стоит добавить его автоматическую генерацию на основе названия, но я решил оставить возможность ручного ввода для большей гибкости выбора адреса.

![View of the demo-admin-country-menu](readme_images/demo-main-page-counries-yorkshire.png)

При нажатии на пункт меню происходит переход по соответствующему url, а также дочерние пункты выбранного становятся видимыми.

![View of the demo-admin-country-menu](readme_images/demo-main-page-countries.png)

## Установка и запуск проекта


***Клонировать репозиторий и перейти в него в командной строке:***

```
git clone git@github.com:your_username_in_github/django_tree_menu.git
```

***Cоздать и активировать виртуальное окружение:***
```
Для Windows:
python -m venv env
source venv/Script/activate

Для Linux/MacOS:
python3 -m venv venv
source venv/bin/activate
```

### Если ваша OS поддерживает Makefile

Если ваша OS поддерживает запуск Makefile, в корневой директории проекта выполните команду

```
make setup
```
В процессе её выполнения будут установлены зависимости, выполнены миграции, установлены фикстуры, а также будет запущен сервер.

Далее при необходимости вы можете создать суперпользователя для просмотра админ панели.

Для этого выполните команду
```
make create-test-admin
```

### Если ваша OS не поддерживает make

***Установить зависимости из файла requirements.txt:***

```
python -m pip install --upgrade pip
pip install -r requirements.txt
```

***Выполнить миграции***

```
python manage.py makemigrations
python manage.py migrate
```

***Загрузить подготовленные фикстуры***
```
python manage.py loaddata data/db.json
```
***Запустить сервер разработки***

```
python manage.py runserver
```

***Создать суперпользователя***

```
python manage.py createsuperuser
```

### Ссылки для просмотра демо

***Зайти в админ панель***

[http://localhost:8000/admin](http://localhost:8000/admin)

***Посмотреть главную страницу с демо меню***

[http://localhost:8000](http://localhost:8000)

## Автор

Бучельников Александр

[![Telegram](https://img.shields.io/badge/-Telegram-black?style=for-the-badge&logo=Telegram)](https://t.me/aleksandr_buchelnikov)
[![LinkedIn](https://img.shields.io/badge/-LinkedIn-black?style=for-the-badge&logo=LinkedIn)](https://www.linkedin.com/in/aleksandr-buchelnikov/)
[![E-mail](https://img.shields.io/badge/-E--mail-black?style=for-the-badge&logo=Gmail)](mailto:al.buchelnikov@gmail.com)