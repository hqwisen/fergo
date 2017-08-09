from django.conf.urls import url

from api.views import ProjectsCollection, TasksCollection

urlpatterns = [
    url(r'projects', ProjectsCollection.as_view()),
    url(r'tasks', TasksCollection.as_view()),

]
