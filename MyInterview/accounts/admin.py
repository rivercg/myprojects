from django.contrib import admin
from models import VirtualUser

class VirtualUserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user_name', 'role', 'username_pk', 'disp_name', 'email', 'last_login')
    list_filter = ['role']
    search_fields = ['role']

admin.site.register(VirtualUser, VirtualUserAdmin)

