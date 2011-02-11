from django.db import models

class StaticPage(models.Model):
    name = models.CharField('Name of the Static',max_length=255,unique=True)
    slug = models.SlugField(unique = True)    
    # title fields
    title = models.CharField(max_length=500, blank=True)
    keywords = models.TextField(blank=True)
    description = models.TextField(blank=True)
    #body fields
    content = models.TextField(blank=True)

    creation_date = models.DateTimeField('Creation date',auto_now_add=True)
    last_modified = models.DateTimeField('Last modification date', auto_now=True)

    def __str__(self):
        return self.name
    
