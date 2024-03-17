from django.db import models


class TaskStatus(models.TextChoices):
    ongoing = "Ongoing"
    completed = "Completed"
    abandoned = "Abandoned"


class Task(models.Model):
    task_id = models.CharField(max_length=50, null=False, unique=True, editable=False)
    project = models.ForeignKey("project.Project", on_delete=models.CASCADE, null=False, related_name="tasks")
    name = models.CharField(max_length=255, null=False)
    due_date = models.DateTimeField(null=True)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=TaskStatus.choices, default=TaskStatus.ongoing)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
