from django.conf.urls import url

from api.views import ListProjects

urlpatterns = [
    url(r'projects/', ListProjects.as_view()),
]
