"""todo_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from todo_django import settings
from todo.views import home, profile, manage_profile, accept_invitation

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/profile', profile, name="profile"),
    url(r'^accounts/manage_profile', manage_profile, name="manage_profile"),
    url(r'^accept_invitation', accept_invitation, name="accept_invitation"),
    url(r'^invitations/', include('invitations.urls',
                                  namespace='invitations')),
    url(r'^todo/', include('todo.urls', namespace='todo')),
    url(r'^api/', include('todo.api.urls')),
    url(r'^$', home, name='home')
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
