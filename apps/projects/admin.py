from django.contrib import admin

# Register your models here.
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'title',
        'employer',
        'budget',
        'status',
        'created_at',
    )

    list_filter = (
        'status',
    )

    search_fields = (
        'title',
    )