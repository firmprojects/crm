from django.urls import path, include
from .views import CreateProject, ProjectDetail, ClientsCreateView, ClientsDetailView, ClientsUpdateView, ClientDelete

app_name = 'project'
urlpatterns = [
    path('create/', CreateProject.as_view(), name='projects'),
    path('<int:pk>/', ProjectDetail.as_view(), name='project_detail'),
    path('clients/', ClientsCreateView.as_view(), name='clients'),
    path('client/<int:pk>/', ClientsDetailView.as_view(), name='client_detail'),
    path('client/update/<int:pk>/', ClientsUpdateView.as_view(), name='edit_client'),
    path('client/delete/<int:pk>/', ClientDelete.as_view(), name='delete_client')
]
