from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404

from staticpage.models import StaticPage

def index(request,slug):
    # TODO We should not show tag list or category list here.
    # those are in blog level.
    # but static page is in application level.
    blog = get_object_or_404(StaticPage,slug=slug)
    tag_list = blog.tag_set.all()
    category_list = blog.category_set.all()

    return render_to_response('staticpage/staticpage_index.html',
                              {'blog':blog,
                               'date_list':BlogPost.view_objects.date_list(),
                               'tag_list':tag_list,
                               'category_list':category_list,
                               'blogpost_set':BlogPost.view_objects.with_teaser().filter(blog=blog),
                               },
                              )

