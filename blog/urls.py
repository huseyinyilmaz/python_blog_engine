from django.conf.urls.defaults import *
import views
urlpatterns = patterns('',
                       url('^(?P<blog_slug>\S+)/tags/(?P<tag_slug>\S+)/$', views.tag, name = 'blog_tag'),

                       url('^(?P<blog_slug>\S+)/(?P<year>\d+)/(?P<month>\d+)/(?P<post_slug>\S+)/$', views.post, name = 'blog_post'),
                       url('^(?P<blog_slug>\S+)/(?P<year>\d+)/(?P<month>\d+)/$', views.month, name = 'blog_month'),
                       url('^(?P<blog_slug>\S+)/$', views.index, name = 'blog_index'),

                       )
