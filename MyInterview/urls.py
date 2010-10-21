from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # admin/doc 
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # admin
    (r'^admin/', include(admin.site.urls)),

    # candidates and jobs
    (r'^candidates/', include('candidates.urls')),
    (r'^jobs/', include('jobs.urls')),
    
    # accounts
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/', include('accounts.urls')),

    # all the others to interview
    (r'', include('interviews.urls')),
)
