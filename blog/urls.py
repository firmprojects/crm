from django.contrib import admin
from django.urls import path
from .views import (
    BlogDeleteView, 
    BlogListView, 
    BlogDetail, 
    CreateBlogView, 
    UpdateBlogView
    )

app_name = 'blog'
urlpatterns = [
    path('', BlogListView.as_view(), name='blog_view'),
    path('detail/<pk>', BlogDetail.as_view(), name='detail'),
    path('<int:pk>/update', UpdateBlogView.as_view(), name='update'),
    path('<int:pk>/delete', BlogDeleteView.as_view(), name='delete'),
    path('create/', CreateBlogView.as_view(), name='add_blog'),

]
