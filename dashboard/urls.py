from django.contrib import admin
from django.urls import path
from .views import Home, Assets, Settings, book_list, book_create

app_name = 'dashboard'
urlpatterns = [
    path('', Home.as_view(), name="home"),
    path('assets', Assets.as_view(), name="assets"),
    path('settings', Settings.as_view(), name="settings"),
    path('books/', book_list, name='book_list'),
    path('books/create/', book_create, name='book_create'),
]