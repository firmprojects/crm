from django.urls import path, include
from .views import *

app_name = 'project'
urlpatterns = [
    path('create/', CreateProject.as_view(), name='projects'),
    path('list/', CreateProjectList.as_view(), name='project-list'),
    path('delete_project/<pk>/',delete_project,name='delete_project'),
    path('upload_doc/<pk>/',upload_doc,name='upload_doc'),
    path('change_priority/',change_priority,name='change_priority'),
    path('change_status/',change_status,name='change_status'),
    path('<int:pk>/', ProjectDetail.as_view(), name='project_detail'),
    path('upload_image/<pk>/',upload_image,name='upload_image'),
    path('clients/', ClientsCreateView.as_view(), name='clients'),
    path('user_autocomplete/', UsersAutocompletesView.as_view(), name="user_autocomplete"),
    path('clients_autocomplete/', ClientAutocompletesView.as_view(), name="client_autocomplete"),
    path('company_autocomplete/',CompanyAutocompletesView.as_view(),name='company_autocomplete'),
    path('project_autocomplete/',ProjectAutocompletesView.as_view(),name='project_autocompletes'),
    path('<pk>/milestones/', milestone_list, name='milestones'),
    path('milestones/add/',add_milestone,name="add_milestone"),
    path('milestones/delete/',delete_milestone,name="delete_milestone"),
    path('milestones/mark_complete/',mark_complete,name='mark_complete'),
    path('milestones/auto_/<pk>/',MilestoneAuto.as_view(),name='milestone_auto'),
    path('milestones/assign_/<pk>/',assign_,name='assign_'),
    path('milestones/followers_/<pk>/',followers_,name='followers_')

]
