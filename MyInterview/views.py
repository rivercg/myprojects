from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

@login_required
def index(request):
    if request.user and request.user.is_active:
        return render_to_response('index.html', {'title': 'Home'})
    else:
        return HttpResponseRedirect('http://www.netis.com.cn')
