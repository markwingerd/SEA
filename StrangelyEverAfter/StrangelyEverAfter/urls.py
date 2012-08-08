from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^gallery/', include('gallery.urls')),
    #url(r'^gallery/$', 'gallery.views.index'),
    #url(r'^gallery/(?P<project_id>\d+)/$', 'gallery.views.project'),
    #url(r'^gallery/(?P<project_id>\d+)/(?P<galleryimage_id>\d+)/$', 'gallery.views.galleryimage'),
    url(r'^admin/', include(admin.site.urls)),

    # This needs to be here in order to display images on the local server
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
)

handler404 = 'django.views.defaults.page_not_found'
handler500 = 'django.views.defaults.server_error'
