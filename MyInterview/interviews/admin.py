from django.contrib import admin
from models import IvRecord, Message

class IvRecordAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['position', 'candidate']}),
        ('Status information', {'fields': ['status', 'text', 'iv_date']}),
        ('Users information', {'fields': ['creator', 'follower', 'watcher_list']}),
        ('Date information', {'fields': ['open_date', 'close_date'], 'classes': ['collapse']}),
    ]
    list_display = ('pk', 'position', 'candidate', 'status', 'text', 'iv_date', 'follower', 'open_date', 'creator', 'close_date')
    list_filter = ['position', 'status', 'creator', 'follower', 'iv_date', 'open_date', 'close_date']
    search_fields = ['position', 'candidate', 'status', 'text', 'creator', 'follower', 'watcher_list']
    date_hierarchy = 'open_date'

class MessageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'ivrecord_pk', 'iv_record', 'ivrecord_status', 'sendfrom_pk', 'send_from', 'sendfrom_email')
    list_filter = ['pub_date']
    search_fields = ['text', 'iv_record', 'send_from']
    date_hierarchy = 'pub_date'

admin.site.register(IvRecord, IvRecordAdmin)
admin.site.register(Message, MessageAdmin)

