from django.db import models
from django.core.urlresolvers import reverse
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django.conf import settings
from time import strftime
import markdown
date_query_posgres="""select 
date_part('month', bp.creation_date), 
date_part('year', bp.creation_date),
count(*)
from blog_blogpost bp
group by date_part('month', bp.creation_date), date_part('year', bp.creation_date)
order by date_part('year', bp.creation_date) DESC, date_part('month', bp.creation_date) DESC
"""
date_query_sqlite="""select 
django_extract('month', bp.creation_date), 
django_extract('year', bp.creation_date),
count(*)
from blog_blogpost bp
group by django_extract('month', bp.creation_date), django_extract('year', bp.creation_date)
order by django_extract('year', bp.creation_date) DESC, django_extract('month', bp.creation_date) DESC
"""
class _Month:
    def __init__(self,month,year,count):
        self.year = int(year)
        self.month = int(month)
        self.count = int(count)
        self.datetime= datetime(self.year,self.month,1)
    def __unicode__(self):
        return str(self)
    def __str__(self):
        return "%s (%d)"%(self.datetime.strftime("%B %Y"),self.count)



class Blog(models.Model):
    name = models.CharField('Name of the Blog',max_length=255)
    slug = models.SlugField()    
    title = models.CharField(max_length=500, blank=True)
    tagline = models.CharField(max_length=500, blank=True)
    description = models.TextField(blank=True)
    creation_date = models.DateTimeField('Creation date',auto_now_add=True)
    last_modified = models.DateTimeField('Last modification date', auto_now=True)

    def __str__(self):
        return self.name
    def getURL(self):
        return reverse('main',kwarkg={'blog_slug':self.slug})

    # def get_date_list(self):
    #     cursor = connection.cursor()
    #     cursor.execute(date_query)
    #     resultset = map(lambda x:_Month(*x),cursor.fetchall())
    #     return resultset
    
class Tag(models.Model):
    name = models.SlugField(max_length=500)
    blog = models.ForeignKey(Blog)
    def __unicode__(self):
        return self.name

class Category(models.Model):
    name = models.SlugField(max_length=500)
    blog = models.ForeignKey(Blog)
    def __unicode__(self):
        return self.name
    
class BlogPostViewManager(models.Manager):
    def get_query_set(self):
        return super(BlogPostViewManager,self).get_query_set().defer('content','teaser').order_by('-creation_date')
    def with_teaser(self):
        return self.defer('content_HTML')
    def with_content(self):
        return self.defer('teaser_HTML')
    def tag(self,tag):
        return self.filter(tags__name=tag)
    def date_list(self):
        cursor = connection.cursor()
        if settings.DATABASE_ENGINE == 'sqlite3':
            cursor.execute(date_query_sqlite)
        elif settings.DATABASE_ENGINE == 'postgresql_psycopg2':
            cursor.execute(date_query_posgres)
        else:#default value will be posgres
            cursor.execute(date_query_posgres)

        resultset = map(lambda x:_Month(*x),cursor.fetchall())
        return resultset

class BlogPost(models.Model):
    title = models.CharField(max_length=500)
    slug = models.SlugField()
    published = models.BooleanField(default=True)
    teaser = models.TextField(blank=True)
    teaser_HTML = models.TextField(blank=True)
    content = models.TextField()
    content_HTML = models.TextField()
    tags = models.ManyToManyField(Tag,blank=True, null=True,)
    categories = models.ManyToManyField(Category,blank=True, null=True,)
    
    blog = models.ForeignKey(Blog)
    creation_date = models.DateTimeField('Creation date', auto_now_add=True)
    last_modified = models.DateTimeField('Last modification date', auto_now=True)
    
    view_objects = BlogPostViewManager()
    objects = models.Manager()

    class Meta():
        unique_together = (("slug", "blog"),)

    def getURL(self):
        return reverse('post',kwarkg={'blog_slug':self.blog.slug,'post_slug':self.slug})
        
    def __str__(self):
        return self.title
        
    def save(self,*args,**kwargs):
        md = markdown.Markdown(output_format='HTML4', extensions=['codehilite'])
        if not self.teaser:
            self.teaser = self.content
        self.teaser_HTML = md.convert(self.teaser)
        md.reset()
        self.content_HTML = md.convert(self.content)
        super(BlogPost,self).save(*args,**kwargs)
