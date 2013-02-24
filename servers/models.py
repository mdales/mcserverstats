import datetime
import os

from django.db import models
from django.contrib.auth.models import User

def random_key():
    return os.urandom(16).encode('hex') 

class Server(models.Model):
    name = models.CharField(max_length=255)
    game_type = models.CharField(max_length=32, choices=(("VANILLA", "Vanilla"), ("TEKKIT", "Tekkit")))
    key = models.CharField(max_length=32, default=random_key)
    
    list_display = ('name', 'game_type')
    
    def __str__(self):
        return self.name
        
    def get_ordered_users(self):
        x = self.login_set.all().order_by('user__username')
        print x
        return x
        

class Login(models.Model):
    user = models.ForeignKey(User)
    server = models.ForeignKey(Server)

    def __str__(self):
        return "%s on %s" % (self.user.username, self.server.name)
        
    def is_online(self):        
        if self.access_set.all().count() == 0:
            return False            
        most_recent = self.access_set.all().order_by('-start_time')[0]        
        return most_recent.end_time == None
        

class Access(models.Model):
    login = models.ForeignKey(Login)
    
    start_time = models.DateTimeField(db_index=True)
    end_time = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        if self.end_time != None:
            return "%s: %s -> %s" % (self.login, self.start_time, self.end_time)
        else:
            return "%s: %s..." % (self.login, self.start_time)
                        
    def duration(self):
        if self.end_time == None:
            return datetime.datetime.now() - self.start_time
        else:
            return self.end_time - self.start_time
            
class Death(models.Model):
    login = models.ForeignKey(Login)
    
    time = models.DateTimeField(db_index=True)
    reason = models.CharField(max_length=255)
    
    def __str__(self):
        return "%s: %s %s" % (self.login.server, self.login.user, self.reason)
        

    