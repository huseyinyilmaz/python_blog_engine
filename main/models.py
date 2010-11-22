from django.db import models
from blog.models import Blog
from staticpages.models import StaticPage

class menu(models.Model):

    PAGE_TYPES =(
        ('SP','static_page'),
        ('BL','blog'),
        )

    page_type = models.CharField('Type of page',
                                 max_length=2,choices=PAGE_TYPES)

    title = models.CharField(max_length=500)
    description = models.CharField(max_length=500)
    enabled = models.BooleanField()
    blog = models.ForeignKey(Blog, null=True, blank=True)
    staticPage = models.ForeignKey(StaticPage,null=True, blank=True)

    
