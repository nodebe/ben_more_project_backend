from rest_framework import serializers
from task.serializers import TaskSerializer
from project.services import ProjectService

from project.models import Project

class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, required=False)
    total_tasks = serializers.IntegerField(required=False)
    completed_tasks = serializers.IntegerField(required=False)

    class Meta:
        model = Project
        fields = ["project_id", "name", "due_date", "description", "status", "tasks", "created_at", 
                  "total_tasks", "completed_tasks"]
        read_only_fields = ["project_id", "created_at", "tasks", "total_tasks", "completed_tasks"]


class ValidateProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = []

    def validate(self, attrs):
        data = attrs.copy()

        pid = self.context.get("pid")

        project_service = ProjectService(None)
        project, error = project_service.fetch_single_by_project_id(project_id=pid)

        if error:
            raise serializers.ValidationError(error, "project_id")
        
        data["project"] = project

        return data
    

class UpdateProjectSerializer(ValidateProjectSerializer):

    class Meta:
        model = Project
        fields = ["name", "due_date", "description", "status"]