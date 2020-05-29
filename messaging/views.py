from django.shortcuts import render
from django.views.generic import ListView, DetailView, View, TemplateView, CreateView, UpdateView

class Compose(TemplateView):
    template_name='messaging/compose.html'

class Inbox(TemplateView):
    template_name='messaging/inbox.html'

class MailView(TemplateView):
    template_name='messaging/mail_view.html'


class Blog(TemplateView):
    template_name='messaging/blog.html'

class BlogView(TemplateView):
    template_name='messaging/blog_view.html'

class AddBlog(TemplateView):
    template_name='messaging/add_blog.html'

class EditBlog(TemplateView):
    template_name='messaging/edit_blog.html'

