from django.conf.urls import url
from .views import (project)

urlpatterns = [
    url(r'^$', project, name='project'),
]
