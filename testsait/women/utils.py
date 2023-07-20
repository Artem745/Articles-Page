from django.db.models import Count

from .models import *


menu = [{'title': "Про сайт", 'url_name': 'about'},
        {'title': "Додати статтю", 'url_name': 'add_page'},
        {'title': "Зворотній зв\'язок", 'url_name': 'contact'}
        ]

# Клас, який містить спільні дані та функції для інших класів, які його успадковують.
class DataMixin:
    # Кількість елементів на одній сторінці при пагінації.
    paginate_by = 3

    # Функція для отримання контексту для шаблону (змінних, які передаються у шаблон).
    # Функція отримує додаткові аргументи у вигляді **kwargs (ключ-значення).
    def get_user_context(self, **kwargs):
        # Створюємо змінну context, що містить всі передані аргументи.
        context = kwargs
        # cats = cache.get('cats')
        # if not cats:
        #     cats = Category.objects.annotate(Count('women'))
        #     cache.set('cats', cats, 60)

        # Отримуємо список категорій та кількість статей у кожній категорії.
        cats = Category.objects.annotate(Count('women'))

        # Створюємо копію меню змінної menu, щоб не змінювати оригінальний список.
        user_menu = menu.copy()

        # Якщо користувач не аутентифікований (не увійшов на сайт),
        # видаляємо з меню пункт "Додати статтю".
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        # Додаємо меню до контексту.
        context['menu'] = user_menu

        # Додаємо список категорій до контексту.
        context['cats'] = cats

        # Якщо в контексті не передано змінну cat_selected,
        # створюємо змінну cat_selected і задаємо значення 0 (по замовчуванню).
        if 'cat_selected' not in context:
            context['cat_selected'] = 0

        # Повертаємо контекст, який містить всі змінні для шаблону.
        return context