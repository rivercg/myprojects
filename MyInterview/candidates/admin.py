from django.contrib import admin
from models import Candidate

class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'birthday', 'married', 'hukou', 'email', 'phone', 'cell_phone', 'create_date')
    list_filter = ['gender', 'married', 'hukou']
    search_fields = ['last_name', 'first_name', 'gender', 'birthday', 'married', 'hukou', 'address', 'email', 'phone', 'cell_phone', 'create_date']
    date_hierarchy = 'birthday'

admin.site.register(Candidate, CandidateAdmin)
