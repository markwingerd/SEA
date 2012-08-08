from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('gallery.views',
    url(r'^$', 'index'),
    url(r'^(?P<project_id>\d+)/$', 'project'),
    url(r'^(?P<project_id>\d+)/(?P<galleryimage_id>\d+)/$', 'galleryimage'),
)

#urlpatterns += staticfiles_urlpatterns()


