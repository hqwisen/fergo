from django.db import models


class Task(models.Model):
    # FIXME put a maxlength for the text field
    title = models.CharField(max_length=100, blank=False)
