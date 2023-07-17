from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from .models import *
from .utils import *

# Create your views here.


class WomenHome(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Головна сторінка')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Women.objects.filter(is_published=True).select_related('cat')#шоб субд не нагружати


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

class AboutView(DataMixin, TemplateView):
    template_name = 'women/about.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Інформація про сайт')
        return dict(list(context.items()) + list(c_def.items()))


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
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



# def contact(request):
#     return HttpResponse("Зворотній зв\'язок")


# def login(request):
#     return HttpResponse("Авторизація")


def pageNotFound(request, exception):
    return HttpResponseNotFound(f"<h1>Сторінка не знайдена :(</h1>")

class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
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
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name),
                                      cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))
        # context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        # context['cat_selected'] = context['posts'][0].cat_id

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Реєстрація')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'women/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизація')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')

class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Зворотній зв\'язок')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')

def logout_user(request):
    logout(request)
    return redirect('login')