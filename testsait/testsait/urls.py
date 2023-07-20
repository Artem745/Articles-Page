"""
URL configuration for testsait project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from testsait import settings
# from women.views import index
# from women.views import categories
from women.views import *
from django.urls import path, include

# Файл, який визначає маршрутизацію (URL patterns) додатку.

# Включає стандартні маршрутизаційні шаблони для адміністративної панелі Django.
urlpatterns = [
    path('admin/', admin.site.urls),

    # Включає маршрутизаційні шаблони з women.urls. women - ім'я додатку (app) для статей про жінок.
    path('', include('women.urls')),

    # Включає маршрутизаційні шаблони для captcha, який використовується для захисту від автоматичних дій ботів.
    path('captcha/', include('captcha.urls')),
]

# У разі, якщо налаштування DEBUG установлено у True (тобто режим розробника), додаємо додатковий маршрут для debug_toolbar, який надає зручні інструменти для відлагодження та профілювання.
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
                      path("__debug__/", include(debug_toolbar.urls)),
                  ] + urlpatterns

    # Додаємо маршрутизаційний шаблон для відображення медіафайлів (зображень, відео тощо) у режимі розробника.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Маршрут, який забезпечує вказівку Django, який вид використовувати для обробки 404 помилки.
handler404 = pageNotFound