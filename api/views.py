from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import FergoUser, ProjectRelation, TaskRelation, Task, Project
import logging

logger = logging.getLogger(__name__)


def is_empty_param(request, param_name):
    param = request.query_params.get(param_name, None)
    return param is None or (param.__class__ == str and len(param.strip()) == 0)


class AbstractCollectionView(APIView):
    def handle_param_errors(self, param, param_name, param_model):
        logger.debug("Handling param errors %s:%s:%s" % (param, param_name, param_model))
        status_code = None
        if param is None or (param.__class__ == str and len(param.strip()) == 0):
            title = 'No %s given' % param_name
            status_code = 400
        elif not param_model.objects.filter(id=param).exists():
            title = "%s doesn't exist" % param_name
            status_code = 400
        if status_code is None:
            return None
        else:
            errors = {
                'title': title,
                'status': status_code
            }
            return errors

    def handle_user_errors(self, user_id):
        return self.handle_param_errors(user_id, 'user', FergoUser)

    def handle_project_errors(self, project_id):
        return self.handle_param_errors(project_id, 'project', Project)

    def fetch_rel_rio_collection(self, user_id):
        data = []
        relation_model = self.get_relation_model()
        resource_type = self.get_resource_type()
        for rel in relation_model.objects.filter(user_id=user_id):
            data.append({'type': resource_type, 'id': rel.object_id})
        return data

    def get_rel_user_rio(self, user_id):
        """
        GET collection of Resource Identifier Object of type Meta.resource_type
        that have a relation with user_id
        :param user_id: user_id to check to relation
        :return: a response_json JSON API content containing a collection of RIO or detected errors
        and the HTTP status_code related to the result
        """
        response_json = {}
        errors = self.handle_user_errors(user_id)
        if errors is None:
            response_json['data'] = self.fetch_rel_rio_collection(user_id)
            status_code = 200
        else:
            response_json['errors'] = errors
            status_code = errors['status']
        return response_json, status_code

    def get_relation_model(self):
        return self.Meta.relation_model

    def get_resource_type(self):
        return self.Meta.resource_type

    def handle_exception(self, exc):
        """
        handle exception raised by rest_framework
        :param exc: APIException
        :return:
        """
        errors = {
            'title': 'API Error',
            'detail': str(exc)
        }
        return Response({'errors': errors}, status=exc.status_code)


class ProjectsCollection(AbstractCollectionView):
    class Meta:
        relation_model = ProjectRelation
        resource_type = 'project'

    def get(self, request):
        """
        Return a collection of projects if given:
            - user_id: returns projects that have a ProjectRelation with user_id
        :param request: contains parameters: user_id
        :return: collection of RIO project
        """
        user_id = request.query_params.get('user_id', None)
        response_json, status_code = self.get_rel_user_rio(user_id)
        return Response(response_json, status=status_code)


class TasksCollection(AbstractCollectionView):
    class Meta:
        relation_model = TaskRelation
        resource_type = 'task'

    def fetch_tasks_rio_collection(self, project_id):
        data = []
        for task in Task.objects.filter(project_id=project_id):
            data.append({'type': self.Meta.resource_type, 'id': task.id})
        return data

    def get_project_tasks_rio(self, project_id):
        response_json = {}
        errors = self.handle_project_errors(project_id)
        if errors is None:
            response_json['data'] = self.fetch_tasks_rio_collection(project_id)
            status_code = 200
        else:
            response_json['errors'] = errors
            status_code = errors['status']
        return response_json, status_code

    def get_tasks_rio(self, project_id, user_id=None):
        logger.debug("gettings tasks rio for project_id=%s, user_id=%s" % (project_id, user_id))
        if user_id is None:
            return self.get_project_tasks_rio(project_id)
        else:
            response_json = {}
            errors_user = self.handle_user_errors(user_id)
            errors_project = self.handle_project_errors(project_id)
            if errors_user is None and errors_project is None:
                status_code = 200
                data = []
                for rel in TaskRelation.objects.filter(user_id=user_id):
                    for task in Task.objects.filter(id=rel.object_id, project_id=project_id):
                        data.append({'type': self.Meta.resource_type, 'id': task.id})
                response_json['data'] = data
            else:
                response_json['errors'] = errors_user if errors_project is None else errors_project
                status_code = response_json['errors']['status']
            return response_json, status_code

    def get(self, request):
        """
        Return a collection of tasks if given:
            - user_id: tasks MUST have a TaskRelation with user_id
            - project_id: tasks MUST be linked to project_id
        :param request: contains parameters: user_id, project_id
        :return: collection of RIO task
        """
        project_id = request.query_params.get('project_id', None)
        user_id = request.query_params.get('user_id', None)
        if not is_empty_param(request, 'project_id') and is_empty_param(request, 'user_id'):
            # project_id only
            response_json, status_code = self.get_tasks_rio(project_id)
        elif not is_empty_param(request, 'user_id') and is_empty_param(request, 'project_id'):
            # user_id only
            response_json, status_code = self.get_rel_user_rio(user_id)
        elif not is_empty_param(request, 'user_id') and not is_empty_param(request, 'project_id'):
            # project_id & user_id
            response_json, status_code = self.get_tasks_rio(project_id, user_id)
        else:
            errors = {
                'title': 'Not implemented',
                'detail': 'Cannot get all tasks.'
            }
            response_json = {'errors': errors}
            status_code = 501  # Not implemented
        return Response(response_json, status=status_code)
