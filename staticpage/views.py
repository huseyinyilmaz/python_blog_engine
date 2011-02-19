from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from staticpage.models import StaticPage
from menu.models import get_menu_items

def index(request,slug):
    staticpage = get_object_or_404(StaticPage,slug=slug)

    page = {
        'title' : staticpage.title,
        }


    return render_to_response('staticpage/staticpage_index.html',
                              {'staticpage':staticpage,
                               'page':page,
                               'menu': get_menu_items(),
                               'path': request.path,
                               },
                              )

