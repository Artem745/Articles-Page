# Generated by Django 4.2.2 on 2023-06-29 12:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='Категорія')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Категорії',
                'verbose_name_plural': 'Категорії',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Women',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('content', models.TextField(blank=True, verbose_name='Текст статті')),
                ('photo', models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Фото')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')),
                ('is_published', models.BooleanField(default=True, verbose_name='Публікація')),
                ('cat', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='women.category', verbose_name='Категорія')),
            ],
            options={
                'verbose_name': 'Відомі жінки',
                'verbose_name_plural': 'Відомі жінки',
                'ordering': ['time_create', 'title'],
            },
        ),
    ]
