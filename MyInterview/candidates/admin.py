from django.contrib import admin
from models import *

class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'birthday', 'married', 'hukou', 'email', 'phone', 'cell_phone', 'create_date')
    list_filter = ['gender', 'married', 'hukou']
    search_fields = ['last_name', 'first_name', 'gender', 'birthday', 'married', 'hukou', 'address', 'email', 'phone', 'cell_phone', 'create_date']
    date_hierarchy = 'birthday'

class FeatureLinkAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'link_digest', 'status', 'mod_date')
    list_filter = ['status', 'mod_date']
    search_fields = ['candidate', 'link_digest', 'status']
    date_hierarchy = 'mod_date'   

admin.site.register(Candidate, CandidateAdmin)
admin.site.register(CandidateAckContactLink, FeatureLinkAdmin)
admin.site.register(CandidateAckSchduleLink, FeatureLinkAdmin)
admin.site.register(CandidateUpdateResumeLink, FeatureLinkAdmin)
