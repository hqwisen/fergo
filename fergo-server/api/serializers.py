from rest_framework_json_api import serializers

from api.models import Project, Task, TaskRelation, ProjectRelation


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class ProjectRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectRelation
        fields = '__all__'


class TaskRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskRelation
        fields = '__all__'
