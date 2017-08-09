from rest_framework import serializers

from api.models import Task, Project


"""
class ProjectSerializer:
    type = 'project'
    class Meta:
        model = Project
        fields = '__all__'

class ProjectRIOSerializer(serializers.ModelSerializer):
    type = 'project'
    class Meta:
        model = Project
        fields = ('id',)

class TaskSerializer(serializers.ModelSerializer):
    type = 'task'
    class Meta:
        model = Task
        fields = '__all__'


class TaskRIOSerializer(serializers.ModelSerializer):
    type = 'task'
    class Meta:
        model = Task
        fields = ('id',)
"""