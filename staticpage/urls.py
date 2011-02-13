from django.conf.urls.defaults import patterns,url
import views
urlpatterns = patterns('',
    url(r'(?P<slug>\S+)/$',views.index,name='staticpage_index'),

)

