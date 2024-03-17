from rest_framework import serializers
from project.services import ProjectService
from task.services import TaskService

from task.models import Task

class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ["task_id", "name", "due_date", "description", "status", "created_at"]
        read_only_fields = ["task_id", "created_at"]

    def validate(self, attrs):
        data = attrs.copy()

        pid = self.context.get("pid")

        project_service = ProjectService(None)
        project, error = project_service.fetch_single_by_project_id(project_id=pid)

        if error:
            raise serializers.ValidationError(error, "project_id")
        
        data["project"] = project

        return data


class ValidateTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = []

    def validate(self, attrs):
        data = attrs.copy()

        tid = self.context.get("tid")

        task_service = TaskService(None)
        task, error = task_service.fetch_single_by_task_id(task_id=tid)

        if error:
            raise serializers.ValidationError(error, "task_id")
        
        data["task"] = task

        return data
    

class UpdateTaskSerializer(ValidateTaskSerializer):

    class Meta:
        model = Task
        fields = ["name", "due_date", "description", "status"]