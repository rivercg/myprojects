from django.conf.urls.defaults import *

urlpatterns = patterns('jobs.views',
    url(r'^$', 'index', name='jobs-root'),
    (r'^(?P<pos_id>\d+)/$', 'detail'),
)
