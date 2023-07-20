from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField

from .models import *

# class AddPostForm(forms.Form):
#     title = forms.CharField(max_length=255, label='Назва', widget=forms.TextInput(attrs={'class': 'form-input'}))
#     slug = forms.SlugField(max_length=255, label='URL')
#     content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), label='Інформація')
#     is_published = forms.BooleanField(label='Публікація', required=False, initial=True)
#     cat = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категорія', empty_label='Категорія не обрана')

# Оголошуємо клас форми AddPostForm, який успадковується від форми ModelForm.
class AddPostForm(forms.ModelForm):
    captcha = CaptchaField()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = "Категорія не обрана"

    # Клас Meta визначає метадані для форми.
    class Meta:
        # Пов'язуємо форму з моделлю Women.
        model = Women
        # Вибираємо поля моделі, які будуть використовуватись у формі.
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat']
        # Використовуємо віджети для полів форми, щоб змінити їх зовнішній вигляд.
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),  # Встановлюємо клас для поля заголовка.
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10})  # Встановлюємо розміри поля вмісту.
        }

    # Метод clean_title використовується для валідації поля title.
    def clean_title(self):
        # Отримуємо введені дані для поля title.
        title = self.cleaned_data['title']

        # Перевіряємо, чи не перевищує довжину введеного заголовка 40 символів.
        # Якщо так, піднімаємо виняток з повідомленням про помилку.
        if len(title) > 40:
            raise ValidationError('Максимальна кількість символів: 40')

        # Повертаємо очищений заголовок.
        return title

    # Метод clean_slug використовується для валідації поля slug (все теж саме шо і з title).
    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if len(slug) > 40:
            raise ValidationError('Максимальна кількість символів: 40')
        return slug


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логін', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логін', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

class ContactForm(forms.Form):
    name = forms.CharField(label='Ім\'я', max_length=255)
    email = forms.EmailField(label='Email')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField()
