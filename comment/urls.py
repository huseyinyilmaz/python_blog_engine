from django.conf.urls.defaults import *
from django.views.decorators.cache import cache_page
import views

urlpatterns = patterns('',
                       url('^(?P<blogpost_id>\d+)/$', views.createComment, name = 'comment_create'),
                       )
