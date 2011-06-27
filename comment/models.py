from django.db import models
from blog.models import BlogPost

class Comment(models.Model):
    verified = models.BooleanField(default=False)
    blogpost = models.ForeignKey(BlogPost)

    name = models.CharField(max_length=500)
    email = models.EmailField()
    emailHash = models.CharField(max_length=500)#used for gravatar

    website = models.URLField(blank=True,null=True)
    value = models.TextField(blank=True)

    creation_date = models.DateTimeField('Creation date', auto_now_add=True)
    last_modified = models.DateTimeField('Last modification date', auto_now=True)

    def __str__(self):
        return "(%s) created at %s"%(self.name,str(self.creation_date))


