from django.conf.urls.defaults import *

urlpatterns = patterns('interviews.views',
    url(r'^$', 'index', name='iv-redords-root'),
    (r'^$', 'index'),
    (r'^active/$', 'active_list'),
    (r'^closed/$', 'closed_list'),
    (r'^add/$', 'add_record'),
    (r'^message/add$', 'add_message'),
    (r'^(?P<iv_id>\d+)/$', 'detail'),
    (r'^(?P<iv_id>\d+)/close/$', 'close_record'),
    (r'^(?P<iv_id>\d+)/reopen/$', 'reopen_record'),
    (r'^(?P<iv_id>\d+)/send_contact/$', 'send_contact'),
    (r'^(?P<iv_id>\d+)/schedule/change$', 'change_schedule'),
    (r'^(?P<iv_id>\d+)/schedule/cancel/$', 'cancel_schedule'),
    (r'^(?P<iv_id>\d+)/schedule/checkin/$', 'iv_checkin'),
)
