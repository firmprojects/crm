from django.contrib import admin
from django.urls import path
from dashboard.views import Home, Assets, Settings

app_name = 'dashboard'
urlpatterns = [
    path('', Home.as_view(), name="home"),
    path('assets', Assets.as_view(), name="assets"),
    path('settings', Settings.as_view(), name="settings"),
]