from django.conf.urls import url

from api.views import ProjectCollection, TaskCollection

urlpatterns = [
    url(r'projects', ProjectCollection.as_view()),
    url(r'tasks', TaskCollection.as_view()),

]
