from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import FergoUser, ProjectRelation, TaskRelation


class AbstractCollectionView(APIView):
    def handle_user_errors(self, user_id):
        status_code = None
        if user_id is None or (user_id.__class__ == str and len(user_id.strip()) == 0):
            title = 'No user given.'
            status_code = 400
        elif not FergoUser.objects.filter(id=user_id).exists():
            title = "User doesn't exist."
            status_code = 400
        if status_code is None:
            return None
        else:
            errors = {
                'title': title,
                'status': status_code
            }
            return errors

    def fetch_rio_collection(self, user_id):
        data = []
        relation_model = self.get_relation_model()
        resource_type = self.get_resource_type()
        for rel in relation_model.objects.filter(user_id=user_id):
            data.append({'type': resource_type, 'id': rel.object_id})
        return data

    def get(self, request):
        response_json = {}
        user_id = request.query_params.get('user_id', None)
        errors = self.handle_user_errors(user_id)
        if errors is None:
            response_json['data'] = self.fetch_rio_collection(user_id)
            status_code = 200
        else:
            response_json['errors'] = errors
            status_code = errors['status']
        return Response(response_json, status=status_code)

    def get_relation_model(self):
        return self.Meta.relation_model

    def get_resource_type(self):
        return self.Meta.resource_type


class ProjectsCollection(AbstractCollectionView):
    class Meta:
        relation_model = ProjectRelation
        resource_type = 'project'

class TasksCollection(AbstractCollectionView):
    class Meta:
        relation_model = TaskRelation
        resource_type = 'task'
