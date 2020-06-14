from django.urls import path, include
from .views import *

app_name = 'tasks'
urlpatterns = [
    path('', Tasks.as_view(), name='tasks'),
    path('detail/<pk>/', TaskDetail.as_view(), name='detail'),
    path('new/', NewTask.as_view(), name='new'),
    path('staff/', StaffTask.as_view(), name='staff_task'),
    path('ticket', TicketingView.as_view(), name='ticket'),
    path('ticket/<str:id>/completed/', TicketCompletedView.as_view(), name='completed'),
    path('ticket/<str:id>/delete/', TicketDeleteView.as_view(), name='delete'),
    path('upload_image/<pk>/',upload_image,name='upload_image'),
    path('upload_doc/<pk>/',upload_doc,name='upload_doc'),

    path('start_task/',start_task,name='start_task'),
    path('end_task/',end_task,name='end_task'),
    path('get_time/',get_time,name='get_time'),
    path('terminate_task/',terminate_task,name='terminate_task'),

    path('change_status/',change_status,name='change_status'),
    path('change_priority/',change_priority,name='change_priority')
]
