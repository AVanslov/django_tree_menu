from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from menu.models import MenuItem

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="homepage/home.html")),
]

try:
    urlpatterns += [
        path(
            str(page.url),
            TemplateView.as_view(template_name="homepage/home.html"),
            name="menu_item_page"
        ) for page in MenuItem.objects.all()
    ]
except Exception:
    print('База данных ещё не создана')
