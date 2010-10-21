from django.conf.urls.defaults import *

urlpatterns = patterns('jobs.views',
    (r'^$', 'index'),
    (r'^(?P<pos_id>\d+)/$', 'detail'),
)
