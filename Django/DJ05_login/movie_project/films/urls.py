from django.urls import path
from . import views
from .views import register
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home_redirect, name='home'),
    path('add/', views.add_movie, name='add_movie'),
    path('list/', views.movie_list, name='movie_list'),
    path('register/', views.register, name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]