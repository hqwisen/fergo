from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class FergoUser(AbstractUser):
    class JSONAPIMeta:
        resource_name = "fergo_user"


class UserProfile(models.Model):
    user = models.OneToOneField(FergoUser, on_delete=models.CASCADE)


class Project(models.Model):
    name = models.CharField(max_length=settings.PROJECT_SETTINGS['name_max_length'], blank=False)
    # TODO find a way to block editing this attribute (after it is created of course)
    creator = models.ForeignKey(FergoUser, blank=False, null=True)

    class JSONAPIMeta:
        resource_name = "project"


class Task(models.Model):
    name = models.CharField(max_length=settings.TASK_SETTINGS['name_max_length'], blank=False)
    project = models.ForeignKey(Project, blank=False, null=True)

    class JSONAPIMeta:
        resource_name = "task"


class ProjectRelation(models.Model):
    object = models.ForeignKey(Project, blank=False, null=True)
    user = models.ForeignKey(FergoUser, blank=False, null=True)
    relation_type = models.IntegerField(default=settings.PROJECT_RELATION['owned'])

    class Meta:
        unique_together = (("object", "user"),)

    class JSONAPIMeta:
        resource_name = "project_relation"


class TaskRelation(models.Model):
    object = models.ForeignKey(Task, blank=False, null=True)
    user = models.ForeignKey(FergoUser, blank=False, null=True)
    relation_type = models.IntegerField(default=settings.TASK_RELATION['owned'])

    class Meta:
        unique_together = (("object", "user"),)

    class JSONAPIMeta:
        resource_name = "task_relation"
