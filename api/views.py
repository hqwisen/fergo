import logging

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from api import utils
from api.models import Task, Project, ProjectRelation, TaskRelation
from api.serializers import ProjectSerializer, TaskSerializer

logger = logging.getLogger(__name__)


class RelationAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Filter the relation objects with the user_id
        given as a request parameter
        :return: queryset of 'model_class' objects
        """
        # user_id = utils.get_int_param(self.request, 'user_id')
        user_id = utils.get_int_param(self.request, 'user_id')
        relations = self.relation_class.objects.filter(user_id=user_id)
        object_ids = [relation.object_id for relation in relations]
        queryset = self.model_class.objects.filter(id__in=object_ids)
        return queryset


class ProjectCollection(RelationAPIView):
    model_class = Project
    serializer_class = ProjectSerializer
    relation_class = ProjectRelation
    pagination_class = None


class TaskCollection(RelationAPIView):
    model_class = Task
    serializer_class = TaskSerializer
    relation_class = TaskRelation
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
