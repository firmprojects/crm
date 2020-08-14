from django.urls import path, include
from .views import CreateCompany

app_name = 'settings'
urlpatterns = [
    path('company_info/', CreateCompany, name='company_info'),
]