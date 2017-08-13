import logging

from django.contrib.auth.models import AnonymousUser
from rest_framework import generics
from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import IsAuthenticated

from api import utils
from api.models import Task, Project, ProjectRelation, TaskRelation
from api.serializers import ProjectSerializer, TaskSerializer, ProjectRelationSerializer, TaskRelationSerializer

logger = logging.getLogger(__name__)


class RelationAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Filter the relation objects with the user_id
        given as a request parameter
        :return: queryset of 'model_class' objects
        """

        # Since IsAuthenticated is in permission_classes -> request.user != None
        if not self.request.user or isinstance(self.request.user, AnonymousUser):
            # This should never happened, and should be catch by 'permission_classes'
            raise NotAuthenticated
        logger.debug("user is: %s" % self.request.user)
        user_id = self.request.user.id
        relations = self.relation_class.objects.filter(user_id=user_id)
        object_ids = [relation.object_id for relation in relations]
        queryset = self.model_class.objects.filter(id__in=object_ids)
        return queryset

    def create(self, request, *args, **kwargs):
        response = super(RelationAPIView, self).create(request, args, kwargs)
        self.create_relation(response.data['id'])
        return response

    def create_relation(self, object_id):
        utils.create_relation(self.relation_class, self.relation_serializer_class,
                              object_id, self.request.user.id)


class ProjectCollection(RelationAPIView):
    model_class = Project
    serializer_class = ProjectSerializer
    relation_class = ProjectRelation
    relation_serializer_class = ProjectRelationSerializer
    pagination_class = None

    def create(self, request, *args, **kwargs):
        request.data['creator'] = {
            'type': 'fergo_user',
            'id': self.request.user.id
        }
        return super(ProjectCollection, self).create(request, args, kwargs)


class TaskCollection(RelationAPIView):
    model_class = Task
    serializer_class = TaskSerializer
    relation_class = TaskRelation
    relation_serializer_class = TaskRelationSerializer
    pagination_class = None

    def get_queryset(self):
        """
        Also filter tasks based on project_id if given as a parameter
        :return:
        """
        # Default queryset is tasks having a relation with the user
        queryset = super(TaskCollection, self).get_queryset()
        project_id = utils.get_int_param(self.request, 'project_id')
        if project_id is not None:
            if queryset is None or not queryset.exists():
                queryset = Task.objects.filter(project_id=project_id)
            else:
                queryset = queryset.filter(project_id=project_id)
        return queryset
