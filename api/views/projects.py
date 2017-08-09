from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import FergoUser, ProjectRelation


class ProjectsCollection(APIView):
    def handle_user_errors(self, user_id):
        # if not FergoUser.objects.exists(user_id=user_id):
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

    def fetch_projects(self, user_id):
        data = []
        for prel in ProjectRelation.objects.filter(user_id=user_id):
            data.append({'type': 'project', 'id': prel.project_id})
        return data

    def get(self, request):
        response_json = {}
        user_id = request.query_params.get('user_id', None)
        errors = self.handle_user_errors(user_id)
        if errors is None:
            response_json['data'] = self.fetch_projects(user_id)
            status_code = 200
        else:
            response_json['errors'] = errors
            status_code = errors['status']
        return Response(response_json, status=status_code)
