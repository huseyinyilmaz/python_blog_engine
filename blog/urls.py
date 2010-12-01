from django.conf.urls.defaults import *
import views
urlpatterns = patterns('',
                       url('^(?P<blog_slug>\S+)/(?P<year>\d+)/(?P<month>\d+)/(?P<post_slug>\S+)/$', views.post, name = 'post'),
                       url('^(?P<blog_slug>\S+)/(?P<year>\d+)/(?P<month>\d+)/$', views.month, name = 'month'),
                       url('^(?P<blog_slug>\S+)/(?P<year>\d+)/$', views.year, name = 'year'),
                       url('^(?P<blog_slug>\S+)/$', views.archive_index, name = 'archive_index'),
                       )
