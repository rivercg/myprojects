from django.contrib import admin
from models import Position

class PositionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['title', 'department', 'closed']}),
        ('Position Detail',  {'fields': ['responsibility', 'requirement', 'preference']}),
        ('Date information', {'fields': ['pub_date', 'close_date'], 'classes': ['collapse']}),
    ]
    list_display = ('title', 'department', 'pub_date', 'was_published_today', 'closed', 'close_date')
    list_filter = ['department', 'closed', 'pub_date']
    search_fields = ['title', 'department', 'responsibility', 'requirement', 'preference']
    date_hierarchy = 'pub_date'

admin.site.register(Position, PositionAdmin)
