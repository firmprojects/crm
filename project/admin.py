from django.contrib import admin
from .models import *


class ProjectsAdmin(admin.ModelAdmin):
    list_display = [
        'project_id', 'name', 'start_date', 'end_date', 'priority',
        'client', 'created_date', 'project_cost', 'budget',
        'priority', 'status', 'planning', 'design', 'development', 'testing',

    ]


class MilestoneAdmin(admin.ModelAdmin):
    list_display = [
        'task', 'project', 'assigned_to'
    ]


admin.site.register(Milestone, MilestoneAdmin)


admin.site.register(IssuesTable)

admin.site.register(RiskTable)


class BudgetRiskAdmin(admin.ModelAdmin):
    list_display = [
        'project', 'amount_budgetted', 'amount_spent', 'amount_over_budget',
    ]


admin.site.register(BudgetRisk, BudgetRiskAdmin)


class PlanningAdmin(admin.ModelAdmin):
    list_display = [
        'deadline', 'status', 'date'
    ]


admin.site.register(Planning, PlanningAdmin)


class DesignAdmin(admin.ModelAdmin):
    list_display = [
        'deadline', 'status', 'date'
    ]


admin.site.register(Design, DesignAdmin)


class DevelopmentAdmin(admin.ModelAdmin):
    list_display = [
        'deadline', 'status', 'date'
    ]


admin.site.register(Development, DevelopmentAdmin)


class TestingAdmin(admin.ModelAdmin):
    list_display = [
        'deadline', 'status', 'date'
    ]


admin.site.register(Testing, TestingAdmin)
