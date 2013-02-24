import datetime
import os

from servers.models import Server, Login, Access, Death
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def join(request, server_key):
    
    try:
        server = Server.objects.get(key=server_key)
    except Server.DoesNotExist:
        raise Http404
    
    if request.method == "POST":
        try:
            username = request.POST['username']
            datetime_str = request.POST['datetime']
        except KeyError:
            raise Http404
            
        try:
            datetime_actual = datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            raise Http404
            
        # is there a user object for this user?
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User.objects.create_user(username=username, password=os.urandom(16).encode('hex'))
            
        # is there a login object for this user/server pair?
        try:
            login = server.login_set.get(user=user)
        except  Login.DoesNotExist:
            login = Login.objects.create(server=server, user=user)
            
        # does an access for this time already exist?
        try:
            access = login.access_set.get(start_time=datetime_actual)
        except Access.DoesNotExist:            
            access = Access.objects.create(login=login, start_time=datetime_actual)
        
    return HttpResponse("OK")
    
    
@csrf_exempt
def leave(request, server_key):
    
    try:
        server = Server.objects.get(key=server_key)
    except Server.DoesNotExist:
        raise Http404
    
    if request.method == "POST":
        try:
            username = request.POST['username']
            datetime_str = request.POST['datetime']
        except KeyError:
            raise Http404
            
        try:
            datetime_actual = datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            raise Http404
            
        # is there a user object for this user?
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User.objects.create_user(username=username, password=os.urandom(16).encode('hex'))
            
        # is there a login object for this user/server pair?
        try:
            login = server.login_set.get(user=user)
        except  Login.DoesNotExist:
            login = Login.objects.create(server=server, user=user)
            
        # find the  most recent access
        if login.access_set.all().count() > 0:
            last_access = login.access_set.all().order_by('-start_time')[0]
            last_access.end_time = datetime_actual
            last_access.save()
            
    return HttpResponse("OK")        
    
    
@csrf_exempt
def died(request, server_key):
    
    try:
        server = Server.objects.get(key=server_key)
    except Server.DoesNotExist:
        raise Http404
    
    if request.method == "POST":
        try:
            username = request.POST['username']
            datetime_str = request.POST['datetime']
            reason = request.POST['reason']
        except KeyError:
            raise Http404
            
        try:
            datetime_actual = datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            raise Http404
            
        # is there a user object for this user?
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User.objects.create_user(username=username, password=os.urandom(16).encode('hex'))
            
        # is there a login object for this user/server pair?
        try:
            login = server.login_set.get(user=user)
        except  Login.DoesNotExist:
            login = Login.objects.create(server=server, user=user)
            
        death = Death.objects.create(login=login, time=datetime_actual, reason=reason)
            
    return HttpResponse("OK")   