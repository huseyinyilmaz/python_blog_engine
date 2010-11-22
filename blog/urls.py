from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       ('^$', 'django.views.generic.simple.direct_to_template',
                        {'template': 'home.html'}),
#                       (r'^$',include('site.main.urls')),
 #                      (r'^blog/',include('site.blog.urls')),
                       )

