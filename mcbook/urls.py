from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',              'servers.views.my_login'),
    url(r'^home/$',         'servers.views.home'),

    url(r'^djangoadmin/', include(admin.site.urls)),
)


urlpatterns += patterns('servers.api',
    url(r'api/([\w]{32})/join/',    'join'),
    url(r'api/([\w]{32})/leave/',   'leave'),
    url(r'api/([\w]{32})/died/',    'died'),
    
    url(r'api/([\w]{32})/online/',   'online'),
)