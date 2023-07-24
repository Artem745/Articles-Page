from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


from testsait.settings import EMAIL_HOST_USER
from .forms import *
from .models import *
from .utils import *
import smtplib
from email.mime.text import MIMEText

# Клас WomenHome успадковує класи DataMixin і ListView для відображення списку жінок на головній сторінці сайту.
class WomenHome(DataMixin, ListView):
    # model вказує на модель, яка буде використовуватись для отримання даних.
    model = Women
    # template_name вказує на шаблон, який буде використовуватись для відображення сторінки.
    template_name = 'women/index.html'
    # context_object_name вказує ім'я змінної контексту, яка буде містити список жінок, який буде виведений у шаблоні.
    context_object_name = 'posts'

    # Метод get_context_data переозначається для додавання додаткових даних до контексту сторінки.
    def get_context_data(self, *, object_list=None, **kwargs):
        # Спочатку викликаємо метод get_context_data батьківського класу, щоб отримати базовий контекст.
        context = super().get_context_data(**kwargs)
        # Викликаємо метод get_user_context з класу DataMixin для додавання додаткових даних користувача до контексту.
        c_def = self.get_user_context(title='Головна сторінка')

        # Об'єднуємо базовий контекст і контекст з додатковими даними користувача.
        return dict(list(context.items()) + list(c_def.items()))

    # Метод get_queryset переозначається для отримання відфільтрованого списку жінок для відображення на головній сторінці.
    def get_queryset(self):
        # Фільтруємо записи моделі Women, щоб отримати лише ті, які мають значення is_published=True.
        # Також використовуємо select_related для попереднього завантаження зв'язаних об'єктів "cat" (категорії) для ефективності.
        return Women.objects.filter(is_published=True).select_related('cat')  #шоб субд не нагружати


# def index(request):
#     posts = Women.objects.all()
#
#     context = {'posts': posts,
#                'menu': menu,
#                'title': 'Головна сторінка',
#                'cat_selected': 0}
#     return render(request, 'women/index.html', context=context)

# def about(request):
#     return render(request, 'women/about.html', {'menu': menu, 'title': 'Про сайт'})
#
# def categoriess(reguest):
#     return HttpResponse(f"<h1>Інформація по категоріям</h1>")
#
# def categories(reguest, catid):
#     if reguest.GET:
#         print(reguest.GET)
#     return HttpResponse(f"<h1>Інформація по категоріям</h1><p>{catid}</p>")
#
# def archive(request, year):
#     if int(year) > 2023:
#         return redirect('home', permanent=True) #без permanent 302, з 301
#         # raise Http404()
#     return HttpResponse(f"<h1>Архів по рокам</h1><p>{year}</p>")

# def about(request):
#     return render(request, 'women/about.html', {'menu': menu, 'title': 'Про сайт'})


# Клас AboutView успадковує класи DataMixin і TemplateView для відображення інформації про сайт.
class AboutView(DataMixin, TemplateView):
    template_name = 'women/about.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Інформація про сайт')
        return dict(list(context.items()) + list(c_def.items()))


# Клас AddPage успадковує класи LoginRequiredMixin, DataMixin і CreateView для додавання статті на сайт.
class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    # form_class вказує на клас форми, яка буде використовуватись для додавання статті.
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Додати статтю')
        return dict(list(context.items()) + list(c_def.items()))

# def add_page(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     return render(request, 'women/addpage.html', {'form': form, 'menu': menu, 'title': "Додати статтю"})

# def назва(request):
#     return HttpResponse("Текст(функція заглушки)")


def pageNotFound(request, exception):
    return HttpResponseNotFound(f"<h1>Сторінка не знайдена :(</h1>")


# Клас ShowPost успадковує класи DataMixin і DetailView для відображення деталей статті.
class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    # slug_url_kwarg вказує на ім'я URL-параметра, який використовується для вибору статті за унікальним слагом.
    slug_url_kwarg = 'post_slug'
    # context_object_name вказує ім'я змінної контексту, яка буде містити об'єкт статті для відображення.
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))

# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#
#     context = {'post': post,
#                'menu': menu,
#                'title': post.title,
#                'cat_selected': post.cat_id}
#     return render(request, 'women/post.html', context=context)


# def show_category(request, cat_slug):
#     posts = Women.objects.filter(cat__slug=cat_slug)
#     if len(posts) == 0:
#         raise Http404()
#
#     context = {'posts': posts,
#                'menu': menu,
#                'title': 'Статті по категоріям',
#                'cat_selected': cat_slug}
#     return render(request, 'women/index.html', context=context)

class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    # context_object_name вказує ім'я змінної контексту, яка буде містити список статей для відображення.
    context_object_name = 'posts'
    # allow_empty вказує, чи дозволяється пустий результат запиту (тобто немає статей в цій категорії).
    allow_empty = False

    # Метод get_queryset переозначається для отримання списку статей, які належать до вибраної категорії.
    def get_queryset(self):
        # Використовуємо метод filter для отримання статей, які мають вказану категорію (slug=self.kwargs['cat_slug'])
        # і які опубліковані (is_published=True). Також використовуємо метод select_related, щоб заздалегідь завантажити категорії,
        # замість додаткових запитів до бази даних для кожної статті.
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # Викликаємо метод get_user_context з класу DataMixin для додавання додаткових даних користувача до контексту.
        # В даному випадку, як заголовок передаємо назву категорії (str(c.name)), яка знаходиться в змінній контексту "c".
        # Також передаємо ідентифікатор категорії (cat_selected=c.pk).
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категорія: ' + str(c.name), cat_selected=c.pk)

        return dict(list(context.items()) + list(c_def.items()))


# Клас RegisterUser успадковує класи DataMixin і CreateView для реєстрації нового користувача.
class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Реєстрація')
        return dict(list(context.items()) + list(c_def.items()))

        # Метод form_valid переозначається для обробки даних з форми після успішної її валідації.
    def form_valid(self, form):
        # Зберігаємо дані з форми і створюємо нового користувача.
        user = form.save()
        # Автоматично виконуємо вхід користувача після успішної реєстрації.
        login(self.request, user)
        return redirect('home')


# Клас LoginUser успадковує класи DataMixin і LoginView для відображення сторінки авторизації користувача.
class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'women/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизація')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


# Клас ContactFormView успадковує клас DataMixin і FormView для відображення сторінки зворотного зв'язку.
class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Зворотній зв\'язок')
        return dict(list(context.items()) + list(c_def.items()))

    # def form_valid(self, form):
    #     # print(form.cleaned_data)
    #     name = form.cleaned_data['name']
    #     email = form.cleaned_data['email']
    #     content = form.cleaned_data['content']
    #     sender = "taknado425@gmail.com"
    #     email_password = "qqxgjadzwmowagnk"
    #     server = smtplib.SMTP("smtp.gmail.com", 587)
    #     server.starttls()
    #     try:
    #         server.login(sender, email_password)
    #         message = f'{name}\n{email}\n{content}'
    #         msg = MIMEText(message)
    #         msg["Subject"] = "Articles-Page. Contact Us"
    #         server.sendmail(sender, sender, msg.as_string())
    #
    #         print("The message was sent successfully!")
    #     except Exception as _ex:
    #         print(f"{_ex}\nCheck your login or password please!")
    #
    #     return redirect('home')

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        content = form.cleaned_data['content']
        send_mail('Articles-Page. Contact Us', f'{name}\n{email}\n{content}', EMAIL_HOST_USER, [EMAIL_HOST_USER])
        return redirect('home')


def logout_user(request):
    logout(request)
    return redirect('login')
