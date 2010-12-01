from django.shortcuts import render_to_response
from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse

import logging

logger = logging.getLogger(__name__)

def index(request,slug=None):
    if slug is None:
        menuItem = Menu.objects.all().order_by('order')[0]
    else:
        menuItem = get_object_or_404(Menu,slug=slug)
    logging.info('slug:' + slug if slug else 'None')
    logging.info('menuItem:' + str(menuItem))

    return HttpResponseRedirect(reverse('staticPageMain')) # Redirect after POST
