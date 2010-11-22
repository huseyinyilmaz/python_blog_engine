from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# urlpatterns = patterns('',
#     # Example:
#     # (r'^python_blog_engine/', include('python_blog_engine.foo.urls')),

#     # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
#     # to INSTALLED_APPS to enable admin documentation:
#     # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

#     # Uncomment the next line to enable the admin:
#     # (r'^admin/', include(admin.site.urls)),

# )



urlpatterns = patterns('',
     (r'^$',include('main.urls')),
    # (r'^blog/',include('blog.urls')),
     (r'^admin/', include('admin.urls')),
     (r'^staticpages/', include('staticpages.urls')),
     (r'^adminorg/doc/', include('django.contrib.admindocs.urls')),
     (r'^adminorg/', include(admin.site.urls)),
     (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
     #(r"^site_media/(?P<path>.*)$", "django.views.static.serve", dict(document_root=settings.MEDIA_ROOT, show_indexes=True)),
 )
