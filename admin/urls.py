from django.conf.urls.defaults import patterns,url
import views
urlpatterns = patterns('',
    url(r'^$',views.index,name='admin_index'),
    url(r'^blogs/$',views.blogMain,name='admin_blogMain'),
    url(r'^bloglist/$',views.blogListMain,name='admin_blogListMain'),
    url(r'^flatpage/$',views.staticPageMain,name='admin_flatPageMain'),

    url(r'^blog/(?P<id>\d+)/$',views.blog,name='admin_blog'),
    url(r'^blog/create/$',views.blogCreate,name='admin_blogCreate'),
    url(r'^blog/edit/(?P<id>\d+)/$',views.blogEdit,name='admin_blogEdit'),
    url(r'^blog/delete/(?P<id>\d+)/$',views.blogDelete,name='admin_blogDelete'),

    # url(r'^staticpage/create/$',views.staticPageCreate,name='admin_staticPageCreate'),
    # url(r'^staticpage/edit/(?P<id>\d+)/$',views.staticPageEdit,name='admin_staticPageEdit'),
    # url(r'^staticpage/delete/(?P<id>\d+)/$',views.staticPageDelete,name='admin_staticPageDelete'),

    url(r'^blogpost/(?P<blog_id>\d+)/create/$',views.blogPostCreate,name='admin_blogPostCreate'),
    url(r'^blogpost/edit/(?P<id>\d+)/$',views.blogPostEdit,name='admin_blogPostEdit'),
    url(r'^blogpost/delete/(?P<id>\d+)/$',views.blogPostDelete,name='admin_blogPostDelete'),

    url(r'^tag/(?P<blog_id>\d+)/$',views.tag,name='admin_tag'),
    # trailing slash problem
    url(r'^tag/(?P<blog_id>\d+)/(?P<id>\d+)$',views.tag,name='admin_tag_update'),
    url(r'^tag/(?P<blog_id>\d+)/(?P<id>\d+)/$',views.tag,name='admin_tag_edit_with_slash'),

    url(r'^category/(?P<blog_id>\d+)/$',views.category,name='admin_category'),
    # trailing slash problem
    url(r'^category/(?P<blog_id>\d+)/(?P<id>\d+)$',views.category,name='admin_category_update'),
    url(r'^category/(?P<blog_id>\d+)/(?P<id>\d+)/$',views.category,name='admin_category_edit_with_slash'),
)
