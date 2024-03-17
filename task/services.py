from task.models import Task, TaskStatus
from services.models_action import ModelAction
from services.utils import CustomApiRequestUtil, generate_id
from django.db.models import Count, F, Q


class TaskService(CustomApiRequestUtil):
    def __init__(self, request):
        self.request = request

    def create(self, payload):
        try:
            payload["task_id"] = generate_id(prefix="TID")

            model_action_service = ModelAction(self.request)

            task, error = model_action_service.create_model_instance(
                model=Task, 
                payload=payload
            )

            if error:
                return None, error
            
            return task, None
        
        except Exception as e:
            return None, self.make_error(error=e)
        
    def update(self, payload):
        try:
            model_action_service = ModelAction(self.request)
            task = payload.pop("task")

            task, error = model_action_service.update_model_instance(
                model_instance=task, **payload
            )

            if error:
                return None, error
            
            return task, None
        
        except Exception as e:
            return None, self.make_error(error=e)
    
    def delete(self, payload):
        try:
            task = payload.get("task")

            task.delete()

            return "Task Deleted Successfully", None

        except Exception as e:
            return None, self.make_error(error=e)
        
    def fetch_single_by_task_id(self, task_id):
        try:
            task = self.get_queryset().get(task_id=task_id)

            return task, None
        
        except Task.DoesNotExist:
            return None, self.make_error(message=f"Task with id: {task_id} does not exist!", status_code=404)    

        except Exception as e:
            return None, self.make_error(error=e)    
        
    def fetch_list(self, filter_params):
        from  task.serializers import TaskSerializer

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

            data = TaskSerializer(page, many=True).data

            return self.get_paginated_list_response(data, queryset.count())

        except Exception as e:
            return None, self.make_error(error=e)
        
    def get_queryset(self):
        return Task.objects
        
    def fetch_options(self):

        options = {
            'status': [{"name": name, "value": value} for name, value in TaskStatus.choices],
        }

        return options