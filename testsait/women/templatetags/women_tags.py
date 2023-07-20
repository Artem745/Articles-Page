from django import template
from women.models import *

# Реєструємо нашу власну бібліотеку з тегами за допомогою декоратора @register.
register = template.Library()


# Оголошуємо простий тег з ім'ям "getcats".
@register.simple_tag(name='getcats')
def get_categories(filter=None):
    if not filter:
        return Category.objects.all()
    else:
        return Category.objects.filter(pk=filter)


# Оголошуємо включаючий тег з ім'ям "show_categories".
@register.inclusion_tag('women/list_categories.html')
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)
    # Повертаємо словник із шаблоном 'women/list_categories.html' та змінними, які можна використовувати в цьому шаблоні.
    # cats - список об'єктів категорій, cat_selected - індекс вибраної категорії (за замовчуванням 0).
    return {"cats": cats, 'cat_selected': cat_selected}
