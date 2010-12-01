from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.views.generic import date_based
from models import Blog
from models import BlogPost
import logging
logger = logging.getLogger(__name__)

def archive_index(request,blog_slug):
    logger.info('slug : ' + blog_slug)
    blog = get_object_or_404(Blog,slug=blog_slug)
    return date_based.archive_index(
        request,
        queryset = blog.blogpost_set.all(),
        date_field = 'creation_date',
        template_name = "blog/blogpost_archive.html",
        template_object_name = "blogpost_set",
        extra_context = {'blog':blog}
    )

def year(request,blog_slug,year):
    logger.info('slug : ' + blog_slug)
    logger.info('year :' + year)
    blog = get_object_or_404(Blog,slug=blog_slug)
    return date_based.archive_year(
        request,
        queryset = blog.blogpost_set.all(),
        date_field = 'creation_date',
        year = year,
        template_name = "blog/blogpost_archive_year.html",
        make_object_list = True,
        template_object_name = "blogpost",
        extra_context = {'blog':blog}
    )

def month(request,blog_slug,year,month):
    logger.info('slug : ' + blog_slug)
    logger.info('year :' + year)
    logger.info('month :' + month)
    blog = get_object_or_404(Blog,slug=blog_slug)
    return date_based.archive_month(
        request,
        queryset = blog.blogpost_set.all(),
        date_field = 'creation_date',
        year = year,
        month = month,
        month_format = '%m',
        template_name = "blog/blogpost_archive_month.html",
        template_object_name = "blogpost",
        extra_context = {'blog':blog}
    )

def post(request,blog_slug,year,month,post_slug):
    logger.info('slug : ' + blog_slug)
    logger.info('year :' + year)
    logger.info('month :' + month)
    blog = get_object_or_404(Blog,slug=blog_slug)
    post = get_object_or_404(BlogPost,blog=blog,slug=post_slug)
    tags = post.tags.all()
    return render_to_response('blog/blogpost.html',
                              {'blog':blog,
                               'blogpost':post,
                               'tags':tags, 
                               })
