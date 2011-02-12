from django.conf.urls.defaults import patterns,url
import views
urlpatterns = patterns('',
    url(r'^/(?P<slug>\S+)$',views.index,name='index'),
    # url(r'^mappingMain/$',views.mappingMain,name='mappingMain'),
    # url(r'^blogs/$',views.blogMain,name='blogMain'),
    # url(r'^flatPages/$',views.flatPagesMain,name='flatPagesMain'),
)

