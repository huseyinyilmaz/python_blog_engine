from django.conf.urls.defaults import *
from main.views import index
urlpatterns = patterns('',
                       url('$^',index,'index'),
                       )
