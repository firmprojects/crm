from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('summernote/', include('django_summernote.urls')),
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('accounts/', include('allauth.urls')),
    path('employees/', include('employees.urls')),
    path('blog/', include('blog.urls')),
    path('crm_accounts/', include('crm_accounts.urls')),
    path('chat/', include('chat.urls')),
    path('project/', include('project.urls', namespace='project')),
    path('messaging/', include('messaging.urls')),
    path('', include('users.urls')),
    path('settings/', include('settings.urls')),
    path('task/', include('tasks.urls')),
    path('books/', include('books.urls')),
]



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
