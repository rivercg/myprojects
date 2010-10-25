from django.conf.urls.defaults import *
from settings import MEDIA_ROOT

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^site_media/$', 'django.views.static.serve', name='site-media-root'),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':MEDIA_ROOT}),
                       
    # admin/doc 
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # admin
    (r'^admin/', include(admin.site.urls)),

    # candidates
    (r'^candidates/', include('candidates.urls')),
    
    # jobs
    (r'^jobs/', include('jobs.urls')),
    
    # accounts
    (r'^accounts/', include('accounts.urls')),

    # all the others to interview
    (r'^interviews/', include('interviews.urls')),
)

urlpatterns += patterns('',
    # all the others to interview
    (r'^$', 'views.index'),
)
