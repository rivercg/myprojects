from django.conf.urls.defaults import *

urlpatterns = patterns('candidates.views',
    (r'^$', 'index'),
    (r'^(?P<candidate_id>\d+)/$', 'detail'),
    (r'^(?P<feature>[A-Z]{2,3})/(?P<digest>\w{6,16})/$', 'featurelink'),
    (r'^(?P<feature>[A-Z]{2,3})/(?P<digest>\w{6,16})/(?P<ack>[TFUC]{1})$', 'ack_featurelink'),
)
