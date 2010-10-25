from django.conf.urls.defaults import *

urlpatterns = patterns('candidates.views',
    url(r'^$', 'index', name='candidates-root'),
    (r'^(?P<candidate_id>\d+)/$', 'detail'),
    (r'^(?P<candidate_id>\d+)/change/$', 'change'),
    (r'^(?P<feature>[A-Z]{2,3})/(?P<digest>\w{6,16})/$', 'featurelink'),
    (r'^(?P<feature>[A-Z]{2,3})/(?P<digest>\w{6,16})/(?P<ack>[TFUC]{1})$', 'ack_featurelink'),
)
