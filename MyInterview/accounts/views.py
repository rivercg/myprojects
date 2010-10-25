from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from models import VirtualUser

@login_required
def index(request):
    # after login, redirect to the interview root
    return HttpResponseRedirect("/") 

@login_required
def users(request):
    latest_users_list = VirtualUser.objects.all().order_by('-real_user__last_login')[:20]
    return render_to_response('accounts/users.html', {'user': request.user, 'title': 'users', 'latest_users_list': latest_users_list})
