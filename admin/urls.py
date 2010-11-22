from django.conf.urls.defaults import patterns,url
import views
urlpatterns = patterns('',
    url(r'^$',views.index,name='index'),
    url(r'^menumain/$',views.menuMain,name='menuMain'),
    url(r'^blogs/$',views.blogMain,name='blogMain'),
    url(r'^staticpage/$',views.staticPageMain,name='staticPageMain'),

    url(r'^staticpage/create/$',views.staticPageCreate,name='staticPageCreate'),
    url(r'^staticpage/edit/(?P<id>\d+)/$',views.staticPageEdit,name='staticPageEdit'),
    url(r'^staticpage/delete/(?P<id>\d+)/$',views.staticPageDelete,name='staticPageDelete'),

)







