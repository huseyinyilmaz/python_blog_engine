from django.shortcuts import get_object_or_404
from staticpage.models import StaticPage
from menu.models import get_menu_items
from django.views.decorators.cache import cache_page
from django.shortcuts import render

@cache_page
def index(request,slug):
    staticpage = get_object_or_404(StaticPage,slug=slug)

    page = {
        'title' : staticpage.title,
        }


    return render( request,
                   'staticpage/staticpage_index.html',
                   {'staticpage':staticpage,
                    'page':page,
                    'menu': get_menu_items(),
                    'path': request.path,
                    },
                   )

