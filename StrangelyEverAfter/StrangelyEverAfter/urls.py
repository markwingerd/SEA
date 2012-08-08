from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^gallery/', include('gallery.urls')),
    #url(r'^gallery/$', 'gallery.views.index'),
    #url(r'^gallery/(?P<project_id>\d+)/$', 'gallery.views.project'),
    #url(r'^gallery/(?P<project_id>\d+)/(?P<galleryimage_id>\d+)/$', 'gallery.views.galleryimage'),
    url(r'^admin/', include(admin.site.urls)),
)

handler404 = 'django.views.defaults.page_not_found'
handler500 = 'django.views.defaults.server_error'
