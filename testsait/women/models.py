from django.db import models
from django.urls import reverse


# Create your models here.

class Women(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    content = models.TextField(blank=True, verbose_name='Текст статті')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d",blank=True, verbose_name='Фото')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')
    is_published = models.BooleanField(default=True, verbose_name='Публікація')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категорія')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = "Відомі жінки"
        verbose_name_plural = "Відомі жінки"
        ordering = ['-time_update','title'] #це навпаки ['time_create','title']норм

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категорія')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = "Категорії"
        verbose_name_plural = "Категорії"
        ordering = ['id']