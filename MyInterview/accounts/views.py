from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return HttpResponse("login user: %s" % request.user)  

def index2(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
            return HttpResponse("Redirect to a success page")  
        else:
            # Return a 'disabled account' error message
            return HttpResponse("Return a 'disabled account' error message")  
    else:
        # Return an 'invalid login' error message.
        return HttpResponse("Return an 'invalid login' error message.")    
