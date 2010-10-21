from django.conf.urls.defaults import *

urlpatterns = patterns('interviews.views',
    (r'^$', 'index'),
)
