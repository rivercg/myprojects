from django.contrib import admin
from models import *

admin.site.register(Message)

class VirtualUserAdmin(admin.ModelAdmin):
    list_display = ('position', 'candidate', 'status', 'open_date', 'close_date')
    list_filter = ['position', 'status', 'open_date', 'close_date']
    search_fields = ['position', 'candidate', 'status']
    date_hierarchy = 'open_date'


class IvRecordAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['position', 'candidate']}),
        ('Status information',  {'fields': ['status']}),
        ('Date information', {'fields': ['open_date', 'close_date'], 'classes': ['collapse']}),
    ]
    list_display = ('position', 'candidate', 'status', 'open_date', 'close_date')
    list_filter = ['position', 'status', 'open_date', 'close_date']
    search_fields = ['position', 'candidate', 'status']
    date_hierarchy = 'open_date'

admin.site.register(VirtualUser, VirtualUserAdmin)
admin.site.register(IvRecord, IvRecordAdmin)

