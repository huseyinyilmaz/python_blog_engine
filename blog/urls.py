from django.conf.urls.defaults import *
from django.views.decorators.cache import cache_page
import views

urlpatterns = patterns('',
                       url('^comment/(?P<id>\d+)/$', views.comment, name = 'blog_post_comment'),

                       url('^(?P<blog_slug>\S+)/tag/(?P<tag_slug>\S+)/$', views.tag, name = 'blog_tag'),
                       url('^(?P<blog_slug>\S+)/(?P<year>\d+)/(?P<month>\d+)/$', views.month, name = 'blog_month'),

                       url('^(?P<blog_slug>\S+)/category/(?P<category_slug>\S+)/$', views.category, name = 'blog_category'),

                       url('^(?P<blog_slug>\S+)/rss/$', cache_page(views.BlogPostRSSFeed()), name = 'blog_rss'),
                       url('^(?P<blog_slug>\S+)/atom/$', cache_page(views.BlogPostAtomFeed()), name = 'blog_atom'),


                       url('^(?P<blog_slug>\S+)/(?P<post_slug>\S+)/$', views.post, name = 'blog_post'),
                       url('^(?P<blog_slug>\S+)/$', views.index, name = 'blog_index'),

                       )
