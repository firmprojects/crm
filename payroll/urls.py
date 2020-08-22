from django.urls import path, include
from .views import *

app_name = 'payroll'
urlpatterns = [
    path('salary/', SalaryView.as_view(), name='salary'),
    path('salary/<int:pk>/', SalaryDetailView.as_view(), name='salary-detail'),


]
