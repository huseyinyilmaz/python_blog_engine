from django.db import models
from django import forms
from blog.models import Blog
from django.contrib.flatpages.models import FlatPage

class Menu(models.Model):
    PAGE_TYPES =(
        ('FP','flatPage'),
        ('BL','blog'),
        )
    
    itemtype = models.CharField('Type of menu item',
                                 max_length=2,choices=PAGE_TYPES)
    order = models.IntegerField(unique=True)
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=500)
    enabled = models.BooleanField()
    blog = models.ForeignKey(Blog, null=True, blank=True)
    flatpage = models.ForeignKey(FlatPage,null=True, blank=True)

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
    fields = ('enabled','itemtype','order','title','description','blog','flatpage')
    # def clean(self):
    #     super(forms.ModelForm,self).clean()
    #     print 'here 2' + self.cleaned_data['itemtype']
    #     return self.cleaned_data

    def clean_blog(self):
        print self.cleaned_data['itemtype']
        if self.cleaned_data['itemtype'] == 'BL':
            if not self.cleaned_data['blog']:
                raise forms.ValidationError("Please choose a blog")
        return self.cleaned_data['blog']

    def clean_flatpage(self):
        if self.cleaned_data['itemtype'] == 'FP':
            if not self.cleaned_data['flatpage']:
                raise forms.ValidationError("Please choose a flatpage")
        return self.cleaned_data['flatpage']
