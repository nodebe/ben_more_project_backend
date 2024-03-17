from django.db import models


class ProjectStatus(models.TextChoices):
    ongoing = "Ongoing"
    completed = "Completed"
    abandoned = "Abandoned"


class Project(models.Model):
    project_id = models.CharField(max_length=50, null=False, unique=True, editable=False)
    name = models.CharField(max_length=255, null=False)
    due_date = models.DateTimeField(null=True)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=ProjectStatus.choices, default=ProjectStatus.ongoing)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
