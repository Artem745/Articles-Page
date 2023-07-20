from django.contrib import admin
from django.utils.safestring import mark_safe

# Register your models here.

from .models import *


# Клас WomenAdmin визначає налаштування адміністративного інтерфейсу для моделі Women.
class WomenAdmin(admin.ModelAdmin):
    # list_display вказує, які поля моделі будуть відображатись у списку записів моделі на сторінці адміністратора.
    list_display = ('id', 'title', 'time_create', 'get_html_photo', 'is_published')

    # list_display_links вказує, які поля моделі мають стати посиланнями на сторінці списку записів моделі.
    list_display_links = ('id', 'title')

    # search_fields вказує, за якими полями моделі буде проводитись пошук записів на сторінці адміністратора.
    search_fields = ('title', 'content')

    # list_editable вказує, які поля моделі можна редагувати безпосередньо зі списку записів моделі на сторінці адміністратора.
    list_editable = ('is_published',)

    # list_filter вказує, за якими полями моделі буде доступний фільтр на сторінці списку записів моделі.
    list_filter = ('is_published', 'time_create')

    # prepopulated_fields вказує, яке поле моделі буде автоматично заповнюватись з іншого поля (зазвичай з slug).
    prepopulated_fields = {"slug": ("title",)}

    # fields вказує, які поля моделі будуть відображатись на сторінці редагування окремого запису моделі.
    fields = (
    'title', 'slug', 'content', 'cat', 'photo', 'get_html_photo', 'is_published', 'time_create', 'time_update')

    # readonly_fields вказує, які поля моделі будуть доступні лише для читання на сторінці редагування окремого запису моделі.
    readonly_fields = ('time_create', 'time_update', 'get_html_photo')

    # save_on_top дозволяє розмістити кнопку "Зберегти" вгорі сторінки редагування запису моделі.
    save_on_top = True

    # Метод get_html_photo визначає, як буде відображатись фотографія у списку записів моделі на сторінці адміністратора.
    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=70>")

    # get_html_photo.short_description вказує назву стовпця для відображення фотографії у списку записів моделі.
    get_html_photo.short_description = "Фото"


# Клас CategoryAdmin визначає налаштування адміністративного інтерфейсу для моделі Category.
class CategoryAdmin(admin.ModelAdmin):
    # list_display вказує, які поля моделі будуть відображатись у списку записів моделі на сторінці адміністратора.
    list_display = ('id', 'name')

    # list_display_links вказує, які поля моделі мають стати посиланнями на сторінці списку записів моделі.
    list_display_links = ('id', 'name')

    # search_fields вказує, за якими полями моделі буде проводитись пошук записів на сторінці адміністратора.
    search_fields = ('name',)

    # prepopulated_fields вказує, яке поле моделі буде автоматично заповнюватись з іншого поля (зазвичай з slug).
    prepopulated_fields = {"slug": ("name",)}


# Реєструємо налаштування адміністративного інтерфейсу для моделей Women і Category.
admin.site.register(Women, WomenAdmin)
admin.site.register(Category, CategoryAdmin)

# Налаштування заголовка та назви адміністративного інтерфейсу Django.
admin.site.site_title = 'Адмін-панель'
admin.site.site_header = 'Адмін-панeль'
