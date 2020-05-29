from django.shortcuts import render
from django.views.generic import ListView, DetailView, View, TemplateView, CreateView, UpdateView

class Chat(TemplateView):
    template_name = 'chat/chat.html'

class VideoCall(TemplateView):
    template_name = 'chat/videocall.html'


class PhoneCall(TemplateView):
    template_name = 'chat/phonecall.html'


class InComingCall(TemplateView):
    template_name = 'chat/incomingcall.html'