from django.contrib import admin
from project.models import Project

# Register your models here.
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["project_id", "name", "due_date", "status"]
    search_fields = ["name", "project_id",]
    
    list_filter = ['due_date', 'status']
    date_hierarchy = "created_at"