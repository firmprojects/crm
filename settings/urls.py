from django.urls import path, include
from .views import *

app_name = 'settings'
urlpatterns = [
    path('company_info/', CreateCompany, name='company_info'),
    path('localization/', LocalizationView.as_view(), name='localization'),
    path('theme-settings/', ThemesettingView.as_view(), name='theme-settings'),
    path('invoice-settings/', InvoicesettingView.as_view(), name='invoice-settings'),
    path('email-settings/', SMTPEmailSettingsView.as_view(), name='email-settings'),
    path('notification-settings/', NotificationSettings.as_view(),
         name='notifications-settings'),
    path('module-settings/', ModuleSettings.as_view(),
         name='module-settings'),
    path('salary-settings/', SalarySettingsView.as_view(), name='salary-settings'),
    path('role-access/', RoleAccessView.as_view(), name='role-access'),
    path('role-delete/<id>/', role_delete, name='role-delete'),
]
