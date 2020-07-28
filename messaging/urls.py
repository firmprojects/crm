from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'messaging'
urlpatterns = [
    path('compose', Compose.as_view(), name='compose'),
    path('inbox', Inbox.as_view(), name='inbox'),
    path('mail-view/<pk>/', MailView.as_view(), name='mail_view'),
    path('mail/<pk>/',MailViewSent.as_view(),name='mail_view_sent'),
    path('blog', Blog.as_view(), name='blog'),
    path('blog-view', BlogView.as_view(), name='blog_view'),
    path('blog-edit', EditBlog.as_view(), name='edit_blog'),
    path('blog-add', AddBlog.as_view(), name='add_blog'),
    path('email/',EmailAutocompletesView.as_view(),name='email_ac'),
    path('reply/<pk>/',ReplyView.as_view(),name='reply_view'),
    path('forward_view/<pk>/',forward_view,name='forward_view'),
    path('mark_as_read/<pk>/',mark_as_read,name='mark_as_read'),
    path('move_to_trash/<pk>/',move_to_trash,name='move_to_trash'),
    path('sent/',Sent_mail.as_view(),name='sent_mail'),
    path('draft/',Draft.as_view(),name='draft_mail'),
    path('trash/',Trash_.as_view(),name='trash_mail'),
    path('empty_trash/',empty_trash,name='empty_trash')

]
