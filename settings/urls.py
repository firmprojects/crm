from django.urls import path, include
from .views import CreateCompany

app_name = 'settings'
urlpatterns = [
    path('company_info/', CreateCompany.as_view(), name='company_info'),
]