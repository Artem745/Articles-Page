from django.views.decorators.cache import cache_page
from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', cache_page(120)(WomenHome.as_view()), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('add_page/', AddPage.as_view(), name='add_page'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', cache_page(120)(WomenCategory.as_view()), name='category'),
]