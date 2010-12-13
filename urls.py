from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    ('^$', 'django.views.generic.simple.direct_to_template',
     {'template': 'index.html','show_indexes':True}),

    (r'^blog/',include('blog.urls')),
    (r'^flatpages/',include('flatpages.urls')),
    (r'^admin2/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin2/', include(admin.site.urls)),
    (r'^admin/',include('admin.urls')),

    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT, 'show_indexes':True}),
    
    )
