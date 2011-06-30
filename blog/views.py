from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404

from django.http import Http404
from django.http import HttpResponse

from models import Blog
from models import BlogPost
from models import Tag
from models import Category
from models import Comment

from forms import CommentForm
from django.utils import simplejson
from menu.models import get_menu_items
import logging
from django.views.decorators.cache import cache_page
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.utils.feedgenerator import Rss201rev2Feed
from django.conf import settings

logger = logging.getLogger(__name__)

@cache_page
def index(request,blog_slug):
    blog = get_object_or_404(Blog,slug=blog_slug)
    tag_list = blog.tag_set.all()
    category_list = blog.category_set.all()

    return render_to_response('blog/blogpost_index.html',
                              {'blog':blog,
                               'date_list':BlogPost.view_objects.date_list(blog.id),
                               'tag_list':tag_list,
                               'category_list':category_list,
                               'blogpost_set':BlogPost.view_objects.with_teaser().filter(blog=blog),
                               'menu': get_menu_items(),
                               'path': request.path,
                               },
                              )

@cache_page
def post(request,blog_slug,post_slug):
    blog = get_object_or_404(Blog,slug=blog_slug)
    try:
        post = BlogPost.view_objects.with_content().get(blog=blog,slug=post_slug)
    except BlogPost.DoesNotExist:
        raise Http404("Blog post does not exist.")

    tag_list = blog.tag_set.all()
    category_list = blog.category_set.all()
    post_tag_list = post.tags.all()
    post_category_list = post.categories.all()
    post_comment_list = post.comment_set.all()
    comment_form = CommentForm()
    return render_to_response('blog/blogpost.html',
                              {'blog':blog,
                               'date_list':BlogPost.view_objects.date_list(blog.id),
                               'tag_list':tag_list,
                               'category_list':category_list,
                               'blogpost':post,
                               'post_tag_list':post_tag_list,
                               'post_category_list':post_category_list,
                               'post_comment_list':post_comment_list,
                               'menu': get_menu_items(),
                               'path': request.path,
                               'form':comment_form,
                               })


def comment(request,id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blogpost_id = id
            comment.save()
            response = {'success':True}
        else:
            response = {'success':False,
                        'form':str(form)}
        return HttpResponse(simplejson.dumps(response))
    return Http404()

@cache_page
def month(request,blog_slug,year,month):
    year = int(year)
    month = int(month)
    
    blog = get_object_or_404(Blog,slug=blog_slug)
    
    date_list = BlogPost.view_objects.date_list(blog.id)
    
    tag_list = blog.tag_set.all()
    category_list = blog.category_set.all()
    
    return render_to_response("blog/blogpost_archive_month.html",
                              {'blog':blog,
                               'date_list':date_list,
                               'tag_list':tag_list,
                               'category_list':category_list,
                               'month':month,
                               'year':year,
                               'blogpost_set':BlogPost.view_objects.with_teaser().filter(blog=blog,creation_date__year=year, creation_date__month=month),
                               'menu': get_menu_items(),
                               'path': request.path,
                               },
                              )

@cache_page
def tag(request,blog_slug,tag_slug):
    
    blog = get_object_or_404(Blog,slug=blog_slug)
    tag = get_object_or_404(Tag,name=tag_slug)
    
    date_list = BlogPost.view_objects.date_list(blog.id)
    tag_list = blog.tag_set.all()
    category_list = blog.category_set.all()
    blogpost_set = BlogPost.view_objects.tag(tag).all()
    
    
    return render_to_response("blog/blogpost_tag.html",
                              {'blog':blog,
                               'date_list':date_list,
                               'tag_list':tag_list,
                               'tag':tag,
                               'category_list':category_list,
                               'blogpost_set':blogpost_set,
                               'menu': get_menu_items(),
                               'path': request.path,
                               },
                              )

@cache_page
def category(request,blog_slug,category_slug):
    
    blog = get_object_or_404(Blog,slug=blog_slug)
    category = get_object_or_404(Category,name=category_slug)
    
    date_list = BlogPost.view_objects.date_list(blog.id)
    tag_list = blog.tag_set.all()
    category_list = blog.category_set.all()
    
    blogpost_set = BlogPost.view_objects.category(category).all()
    
    return render_to_response("blog/blogpost_tag.html",
                              {'blog':blog,
                               'date_list':date_list,
                               'tag_list':tag_list,
                               'category':category,
                               'category_list':category_list,
                               'blogpost_set':blogpost_set,
                               'menu': get_menu_items(),
                               'path': request.path,
                               },
                              )


 #########
 # FEEDS #
 #########
class BlogPostRSSFeed(Feed):
    feed_type = Rss201rev2Feed
    # general feed methods
    def get_object(self, request, blog_slug):
        print 'get_object'
        return get_object_or_404(Blog,slug=blog_slug)
    
    def title(self,obj):
        return "%s - %s"%(settings.TITLE,obj.title)
    
    def description(self,obj):
        return obj.description
    
    def link(self,obj):
        return obj.get_absolute_url()
    
     #item methods
    def items(self,obj):
        return obj.blogpost_set.all().order_by('creation_date')[:1000]
    
    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        return item.teaser_HTML
     
    def item_link(self,item):
        return item.get_absolute_url()
     
class BlogPostAtomFeed(BlogPostRSSFeed):
    feed_type = Atom1Feed
    subtitle = BlogPostRSSFeed.description

