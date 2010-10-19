from django.contrib import admin
from models import Message, VirtualUser, IvRecord


class VirtualUserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user_name', 'role', 'username_pk', 'disp_name', 'email', 'last_login')
    list_filter = ['role']
    search_fields = ['role']

class IvRecordAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['position', 'candidate']}),
        ('Status information',  {'fields': ['status']}),
        ('Date information', {'fields': ['open_date', 'close_date'], 'classes': ['collapse']}),
    ]
    list_display = ('pk', 'position', 'candidate', 'status', 'open_date', 'close_date')
    list_filter = ['position', 'status', 'open_date', 'close_date']
    search_fields = ['position', 'candidate', 'status']
    date_hierarchy = 'open_date'

class MessageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'ivrecord_pk', 'iv_record', 'ivrecord_status', 'sendfrom_pk', 'send_from', 'sendfrom_email')
    list_filter = ['pub_date']
    search_fields = ['text', 'iv_record', 'send_from']
    date_hierarchy = 'pub_date'

admin.site.register(VirtualUser, VirtualUserAdmin)
admin.site.register(IvRecord, IvRecordAdmin)
admin.site.register(Message, MessageAdmin)

