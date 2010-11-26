from django.db import models
from django import forms


class Blog(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    title = models.CharField(max_length=500, blank=True)
    description = models.TextField(blank=True)
    creation_date = models.DateTimeField('Creation date',auto_now_add=True)
    last_modified = models.DateTimeField('Last modification date', auto_now=True)
    def __str__(self):
        return self.name
class Tag(models.Model):
    name = models.CharField(max_length=500)
    def __unicode__(self):
        return self.name

class BlogPost(models.Model):
    title = models.CharField(max_length=500)
    slug = models.SlugField()
    published = models.BooleanField()
    teaser = models.TextField()
    teaser_HTML = models.TextField()
    content = models.TextField()
    content_HTML = models.TextField()
    tags = models.ManyToManyField(Tag)
    blog = models.ForeignKey(Blog)
    creation_date = models.DateTimeField('Creation date',auto_now_add=True)
    last_modified = models.DateTimeField('Last modification date', auto_now=True)


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('name','slug','title','description')


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ('published','blog','title','slug','content','teaser','tags')

