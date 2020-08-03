from django.contrib import admin
from .models import CustomUser, Assets

admin.site.register(CustomUser)
admin.site.register(Assets)

