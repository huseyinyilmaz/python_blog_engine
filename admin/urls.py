from django.conf.urls.defaults import patterns,url
import views
urlpatterns = patterns('',
    url(r'^$',views.index,name='index'),
    url(r'^menumain/$',views.menuMain,name='menuMain'),
    url(r'^blogs/$',views.blogMain,name='blogMain'),
    url(r'^bloglist/$',views.blogListMain,name='blogListMain'),
    url(r'^blogposts/(?P<id>\d+)/$',views.blogPostMain,name='blogPostMain'),
    url(r'^staticpage/$',views.staticPageMain,name='staticPageMain'),

    url(r'^staticpage/create/$',views.staticPageCreate,name='staticPageCreate'),
    url(r'^staticpage/edit/(?P<id>\d+)/$',views.staticPageEdit,name='staticPageEdit'),
    url(r'^staticpage/delete/(?P<id>\d+)/$',views.staticPageDelete,name='staticPageDelete'),

    url(r'^blog/create/$',views.blogCreate,name='blogCreate'),
    url(r'^blog/edit/(?P<id>\d+)/$',views.blogEdit,name='blogEdit'),
    url(r'^blog/delete/(?P<id>\d+)/$',views.blogDelete,name='blogDelete'),

    url(r'^blogpost/(?P<blog_id>\d+)/create/$',views.blogPostCreate,name='blogPostCreate'),
    url(r'^blogpost/edit/(?P<id>\d+)/$',views.blogPostEdit,name='blogPostEdit'),
    url(r'^blogpost/delete/(?P<id>\d+)/$',views.blogPostDelete,name='blogPostDelete'),

    url(r'^tag/create/$',views.blogCreate,name='tagCreate'),
    url(r'^tag/edit/(?P<id>\d+)/$',views.blogEdit,name='tagEdit'),
    url(r'^tag/delete/(?P<id>\d+)/$',views.blogDelete,name='tagDelete'),
                       )







