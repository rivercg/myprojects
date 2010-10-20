from django.shortcuts import render_to_response
from models import Position

def index(request):
    latest_position_list = Position.objects.all().order_by('-pub_date')[:20]
    return render_to_response('jobs/index.html', {'latest_position_list': latest_position_list})
    
def detail(request, pos_id):
    p = Position.objects.get(pk=pos_id)
    return render_to_response('jobs/detail.html', {'pos': p})

def get_job_url(pos):
    return 'jobs/%d/' % pos.pk