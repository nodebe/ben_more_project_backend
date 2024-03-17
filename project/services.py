from task.models import TaskStatus
from project.models import Project, ProjectStatus
from services.models_action import ModelAction
from services.utils import CustomApiRequestUtil, generate_id
from django.db.models import Count, F, Q, ExpressionWrapper, fields


class ProjectService(CustomApiRequestUtil):
    def __init__(self, request):
        self.request = request

    def create(self, payload):
        try:
            payload["project_id"] = generate_id(prefix="PID")

            model_action_service = ModelAction(self.request)

            project, error = model_action_service.create_model_instance(
                model=Project, 
                payload=payload
            )

            if error:
                return None, error
            
            return project, None
        
        except Exception as e:
            return None, self.make_error(error=e)
        
    def update(self, payload):
        try:
            model_action_service = ModelAction(self.request)
            project = payload.pop("project")

            project, error = model_action_service.update_model_instance(
                model_instance=project, **payload
            )

            if error:
                return None, error
            
            return project, None
        
        except Exception as e:
            return None, self.make_error(error=e)
    
    def delete(self, payload):
        try:
            project = payload.get("project")

            project.delete()

            return "Project Deleted Successfully", None

        except Exception as e:
            return None, self.make_error(error=e)
        
    def fetch_single_by_project_id(self, project_id):
        try:
            project = self.get_queryset().get(project_id=project_id)

            return project, None
        
        except Project.DoesNotExist:
            return None, self.make_error(message=f"Project with id: {project_id} does not exist!", status_code=404)    

        except Exception as e:
            return None, self.make_error(error=e)    
        
    def fetch_list(self, filter_params):
        from  project.serializers import ProjectSerializer

        try:
            self.page_size = filter_params.get("page_size", 15)
            status = filter_params.get("status")
            from_date = filter_params.get("from_date")
            to_date = filter_params.get("to_date")
            keyword = filter_params.get("keyword")

            q = Q()

            if status:
                q &= Q(status=status)
            
            if from_date:
                q &= Q(created_at__gte=from_date)

            if to_date:
                q &= Q(created_at__lte=to_date)

            if keyword:
                q &= Q(name__icontains=keyword) | Q(description__icontains=keyword)


            queryset = self.get_queryset().filter(q).order_by("-created_at")

            page = self.paginate_queryset(queryset, request=self.request)

            data = ProjectSerializer(page, many=True).data

            return self.get_paginated_list_response(data, queryset.count())

        except Exception as e:
            return None, self.make_error(error=e)
        
    def get_queryset(self):

        return Project.objects.annotate(
            total_tasks = Count("tasks"),
            completed_tasks = Count("tasks", filter=Q(tasks__status=TaskStatus.completed))
        )

        
    def fetch_options(self):

        options = {
            'status': [{"name": name, "value": value} for name, value in ProjectStatus.choices],
        }

        return options