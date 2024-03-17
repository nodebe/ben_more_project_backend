from task.serializers import TaskSerializer, UpdateTaskSerializer, ValidateTaskSerializer
from services.utils import CustomApiRequestUtil
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView
from task.services import TaskService

class TaskApiView(CreateAPIView, UpdateAPIView, RetrieveAPIView, CustomApiRequestUtil):
    response_serializer = TaskSerializer
    serializer_class = TaskSerializer

    def post(self, request, *args, **kwargs):
        service = TaskService(request)

        self.extra_context_data = {"pid": kwargs.get("pid")}

        return self.process_request(request, service.create)
    
    def put(self, request, *args, **kwargs):
        self.serializer_class = UpdateTaskSerializer
        self.extra_context_data = {"tid": kwargs.get("tid")}

        service = TaskService(request)

        return self.process_request(request, service.update)
    
    def get(self, request, *args, **kwargs):
        self.response_serializer = None

        filter_params = self.get_request_filter_params(request)

        service = TaskService(request)
        tid = kwargs.get("tid")

        if tid:
            self.wrap_response_in_data_object = True
            self.response_serializer = TaskSerializer

            return self.process_request(request, service.fetch_single_by_task_id, task_id=tid)

        return self.process_request(request, service.fetch_list, filter_params=filter_params)
    
    def delete(self, request, *args, **kwargs):
        self.serializer_class = ValidateTaskSerializer
        self.response_serializer = None

        service = TaskService(request)

        self.extra_context_data = {"tid": kwargs.get("tid")}

        return self.process_request(request, service.delete)
    

class TaskOptionsApiView(RetrieveAPIView, CustomApiRequestUtil):

    def get(self, request, *args, **kwargs):
        service = TaskService(request)
        response_data = service.fetch_options()

        return self.response_with_json(response_data)
