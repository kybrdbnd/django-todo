from django.conf.urls import url
from .views import (project, send_invite)

urlpatterns = [
    url(r'^$', project, name='project'),
    url(r'^send_invite/', send_invite, name='send_invite'),
]
