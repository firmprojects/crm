from django.urls import path

from .views import book_create, book_delete, book_list, book_update

urlpatterns = [
    path('', book_list, name='book_list'),
    path('create/', book_create, name='book_create'),
    path('<pk>/update/', book_update, name='book_update'),
    path('<pk>/delete/', book_delete, name='book_delete'),
]