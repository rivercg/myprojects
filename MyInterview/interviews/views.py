from django.http import HttpResponse

def index(request):
    return HttpResponse("interviews. You're at the interviews index.")    
