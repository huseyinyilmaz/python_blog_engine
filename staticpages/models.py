from django.db import models
from django import forms
from django.template.defaultfilters import slugify

class StaticPage(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()

    content_HTML = models.TextField()

    creation_date = models.DateTimeField('Creation date',auto_now_add=True)
    last_modified = models.DateTimeField('Last modification date', auto_now=True)
    def __str__(self):
        return self.name
    
class StaticPageForm(forms.ModelForm):
    class Meta:
        model = StaticPage
        fields = ('name','description','content_HTML')

    def clean(self):
        super(StaticPageForm,self).clean()
        self.cleaned_data['slug'] = slugify(self.cleaned_data['name'])
        return self.cleaned_data

