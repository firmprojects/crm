from django.contrib import admin


from .models import Projects, Clients


class ProjectsAdmin(admin.ModelAdmin):
    list_display = ['name',  'deadline', 'priority', "created_date", "project_cost", "status", "project_leader",]


admin.site.register(Projects, ProjectsAdmin)

admin.site.register(Clients)



