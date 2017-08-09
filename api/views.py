from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Project


class ProjectsCollection(APIView):

    def get(self, request):
        print()
        user_id = request.query_params.get('user_id', None)
        response_json = {}
        status_code = None
        if user_id is None:
            status_code = 400
            errors = {
                'title': 'Bad user',
                'detail': 'No user given.',
                'status': status_code
            }
            response_json['errors'] = errors
        else:
            data = []
            for project in Project.objects.all():
                data.append({'type': 'project', 'id': project.id})
            response_json['data'] = data
            status_code = 200
        return Response(response_json, status=status_code)