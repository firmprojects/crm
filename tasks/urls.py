from django.urls import path, include
from .views import Tasks, TaskDetail, NewTask, StaffTask, TicketingView, TicketCompletedView, TicketDeleteView

app_name = 'tasks'
urlpatterns = [
    path('', Tasks.as_view(), name='tasks'),
    path('detail/', TaskDetail.as_view(), name='detail'),
    path('new/', NewTask.as_view(), name='new'),
    path('staff/', StaffTask.as_view(), name='staff_task'),
    path('ticket/', TicketingView.as_view(), name='ticket'),
    path('ticket/<str:id>/completed/', TicketCompletedView.as_view(), name='completed'),
    path('ticket/<str:id>/delete/', TicketDeleteView.as_view(), name='delete'),
]
