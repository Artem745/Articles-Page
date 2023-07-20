from django.apps import AppConfig


# Клас WomenConfig успадковує властивості класу AppConfig для налаштування додатку "women".
class WomenConfig(AppConfig):
    # Встановлюємо поле default_auto_field для задання типу автоматичного поля бази даних.
    # В даному випадку використовуємо django.db.models.BigAutoField для автоматичного поля.
    default_auto_field = 'django.db.models.BigAutoField'

    # Встановлюємо ім'я додатку, яке використовуватиметься Django.
    name = 'women'

    # Встановлюємо зрозумілу (читабельну) назву для додатку "women".
    verbose_name = 'Жінки'
