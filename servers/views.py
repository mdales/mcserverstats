from django.template import RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response

from servers.models import Server, Login, Access, Death


def my_login(request):
    
    if request.user and request.user.is_authenticated():
        return HttpResponseRedirect('/home/')
        
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)

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

    return render_to_response('home.html', 
        {'logins': login_list},
        context_instance=RequestContext(request))
        
        
@login_required
def server_api(request, server_id):

    print dir(request)

    # check that the user has as login here
    try:
        server = Server.objects.get(id=server_id)
    except Server.DoesNotExist:
        raise Http404
        
    try:
        login = server.login_set.get(user=request.user)
    except Login.DoesNotExist:
        raise Http404
        
    return render_to_response("server_api.html", 
        {'server': server, 'host': request.get_host()},
        context_instance=RequestContext(request))
    