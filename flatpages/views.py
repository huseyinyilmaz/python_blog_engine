from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404

from django.contrib.flatpages.models import FlatPage

import logging
logger = logging.getLogger(__name__)

def main(request,slug):
    slug = '/' + slug
    logger.info("slug : " + slug)
    page = get_object_or_404(FlatPage,url=slug)
    logger.info('flatpage found. pk : ' + str(page.pk))
    return render_to_response('flatpages/main.html',
                              {'page':page})

