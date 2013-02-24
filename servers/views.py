from django.template import RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response

from servers.models import Server, Login, Access, Death


def my_login(request):
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        print user
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/home/')
                
    return render_to_response('login.html', 
        context_instance=RequestContext(request))
        
@login_required
def home(request):
    
    user = request.user
    login_list = user.login_set.all().order_by('server__name')
    print login_list
    return render_to_response('home.html', 
        {'logins': login_list},
        context_instance=RequestContext(request))