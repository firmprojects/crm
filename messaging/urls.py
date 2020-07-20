from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'messaging'
urlpatterns = [
    path('compose', Compose.as_view(), name='compose'),
    path('inbox', Inbox.as_view(), name='inbox'),
    path('mail-view/<pk>/', MailView.as_view(), name='mail_view'),
    path('blog', Blog.as_view(), name='blog'),
    path('blog-view', BlogView.as_view(), name='blog_view'),
    path('blog-edit', EditBlog.as_view(), name='edit_blog'),
    path('blog-add', AddBlog.as_view(), name='add_blog'),
    path('email/',EmailAutocompletesView.as_view(),name='email_ac'),

    ]
