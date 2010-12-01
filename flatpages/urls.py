from django.conf.urls.defaults import *
import views
urlpatterns = patterns('',
                       url('^(?P<slug>\S+)$', views.main,{},'main'),
                       )
