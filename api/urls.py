from django.conf.urls import url

from api.views import ProjectsCollection

urlpatterns = [
    url(r'projects', ProjectsCollection.as_view()),
]
