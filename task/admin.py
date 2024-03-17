from django.contrib import admin
from task.models import Task

# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["task_id", "name", "due_date", "status"]
    search_fields = ["name", "task_id",]
    
    list_filter = ['due_date', 'status']
    date_hierarchy = "created_at"