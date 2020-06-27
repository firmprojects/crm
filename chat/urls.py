from django.contrib import admin
from django.urls import path
from .views import Chat, VideoCall, PhoneCall, InComingCall

app_name = 'chat'
urlpatterns = [
    path('chat', Chat.as_view(), name='chat'),
    path('videocall', VideoCall.as_view(), name='videocall'),
    path('phonecall', PhoneCall.as_view(), name='phonecall'),
    path('incomingcall', InComingCall.as_view(), name='incomingcall'),
]