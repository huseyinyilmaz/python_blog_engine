from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'staticpage.views.index',{'slug':'main'},name='index' ),

    (r'^blog/',include('blog.urls')),
    (r'^sp/',include('staticpage.urls')),
    (r'^c/',include('comment.urls')),
    (r'^admin2/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin2/', include(admin.site.urls)),
    (r'^admin/',include('admin.urls')),

    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT, 'show_indexes':True}),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'},name='login'),    
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login',name='logout'),    
    )
