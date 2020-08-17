from django.contrib import admin


from .models import Projects, Clients


class ProjectsAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'deadline', 'priority']


admin.site.register(Projects, ProjectsAdmin)

admin.site.register(Clients)



