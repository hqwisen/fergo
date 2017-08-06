from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class FergoUser(User):
    pass


class UserProfile():
        user = models.OneToOneField(FergoUser, on_delete=models.CASCADE)


class Project(models.Model):
    name = models.CharField(max_length=settings.PROJECT_SETTINGS['name_max_length'], blank=False)
    users_id = models.ForeignKey(FergoUser)


class Task(models.Model):
    # FIXME put a maxlength for the text field
    title = models.CharField(max_length=settings.TASK_SETTINGS['name_max_length'], blank=False)
    projects_id = models.ForeignKey(Project)
