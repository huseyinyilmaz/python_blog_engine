from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.http import Http404
from models import Blog
from models import BlogPost
from models import Tag
from models import Category
from menu.models import get_menu_items
import logging
from django.views.decorators.cache import cache_page

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
def post(request,blog_slug,year,month,post_slug):
    blog = get_object_or_404(Blog,slug=blog_slug)
    try:
        post = BlogPost.view_objects.with_content().get(blog=blog,slug=post_slug)
    except BlogPost.DoesNotExist:
        raise Http404("Blog post does not exist.")

    tag_list = blog.tag_set.all()
    category_list = blog.category_set.all()
    post_tag_list = post.tags.all()
    post_category_list = post.categories.all()
    return render_to_response('blog/blogpost.html',
                              {'blog':blog,
                               'date_list':BlogPost.view_objects.date_list(blog.id),
                               'tag_list':tag_list,
                               'category_list':category_list,
                               'blogpost':post,
                               'post_tag_list':post_tag_list,
                               'post_category_list':post_category_list,
                               'menu': get_menu_items(),
                               'path': request.path,
                               })

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


