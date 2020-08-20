from django.urls import path, include
from .views import *

app_name = 'settings'
urlpatterns = [
    path('company_info/', CreateCompany, name='company_info'),
    path('localization/', LocalizationView.as_view(), name='localization'),
]