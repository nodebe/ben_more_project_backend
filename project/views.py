from project.serializers import ProjectSerializer, UpdateProjectSerializer, ValidateProjectSerializer
from services.utils import CustomApiRequestUtil
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView
from project.services import ProjectService

class ProjectApiView(CreateAPIView, UpdateAPIView, RetrieveAPIView, CustomApiRequestUtil):
    response_serializer = ProjectSerializer
    serializer_class = ProjectSerializer

    def post(self, request, *args, **kwargs):
        service = ProjectService(request)

        return self.process_request(request, service.create)
    
    def put(self, request, *args, **kwargs):
        self.serializer_class = UpdateProjectSerializer
        self.extra_context_data = {"pid": kwargs.get("pid")}

        service = ProjectService(request)

        return self.process_request(request, service.update)
    
    def get(self, request, *args, **kwargs):
        self.response_serializer = None

        filter_params = self.get_request_filter_params(request)

        service = ProjectService(request)
        pid = kwargs.get("pid")

        if pid:
            self.wrap_response_in_data_object = True
            self.response_serializer = ProjectSerializer

            return self.process_request(request, service.fetch_single_by_project_id, project_id=pid)

        return self.process_request(request, service.fetch_list, filter_params=filter_params)
    
    def delete(self, request, *args, **kwargs):
        self.serializer_class = ValidateProjectSerializer
        self.response_serializer = None

        service = ProjectService(request)

        self.extra_context_data = {"pid": kwargs.get("pid")}

        return self.process_request(request, service.delete)
    

class ProjectOptionsApiView(RetrieveAPIView, CustomApiRequestUtil):

    def get(self, request, *args, **kwargs):
        service = ProjectService(request)
        response_data = service.fetch_options()

        return self.response_with_json(response_data)
