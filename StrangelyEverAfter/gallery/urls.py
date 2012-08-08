from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

urlpatterns = patterns('gallery.views',
    url(r'^$', 'index'),
    url(r'^(?P<project_id>\d+)/$', 'project'),
    url(r'^(?P<project_id>\d+)/(?P<picture_id>\d+)/$', 'picture'),
)

#urlpatterns += staticfiles_urlpatterns()


