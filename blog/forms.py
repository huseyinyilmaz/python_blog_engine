from django import forms
from models import Blog
from models import BlogPost
from django.template.defaultfilters import slugify
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
from django.db.models import Q

class BlogErrorList(forms.util.ErrorList):
    def as_ul(self):
        if not self: return u''
        return mark_safe(u'<div ><ul class="ui-state-error ui-corner-all">%s</ul></div>'
                % ''.join([u'<li class="list"><span style="float: left; margin-right: 0.3em;" class="ui-icon ui-icon-alert"></span>%s</li>' % conditional_escape(force_unicode(e)) for e in self]))

class BlogForm(forms.ModelForm):
    name=forms.CharField(widget=forms.TextInput(attrs={'class':'grid_7'}))
    slug=forms.CharField(widget=forms.TextInput(attrs={'class':'grid_7'}),required=False)
    title=forms.CharField(widget=forms.TextInput(attrs={'class':'grid_7'}))
    tagline=forms.CharField(widget=forms.Textarea(attrs={'class':'grid_7','cols':'','rows':'3'}))
    description=forms.CharField(widget=forms.Textarea(attrs={'class':'grid_7','cols':'','rows':'10'}))

    class Meta:
        model = Blog

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        slug = slugify(slug if slug else self.cleaned_data['name'])
        self.cleaned_data['slug'] = slug
        # if another object with same slug exist and has different id show error
        query = Q(slug = slug)
        if self.instance.id:
            query = query & ~Q(id=self.instance.id)

        if Blog.objects.filter(query).exists():
            raise forms.ValidationError('There is another blog with the same slug')
        return self.cleaned_data['slug']

    def clean_name(self):
        # if another object with same name exist and has different id show error
        query = Q(name = self.cleaned_data['name'])
        if self.instance.id:
            query = query & ~Q(id=self.instance.id)

        if Blog.objects.filter(query).exists():
            raise forms.ValidationError('There is another blog with the same name')
        return self.cleaned_data['name']

    def __init__(self, *args, **kwargs):
        kwargs_new = {'error_class': BlogErrorList}
        kwargs_new.update(kwargs)
        super(BlogForm, self).__init__(*args, **kwargs_new)

##################################################
class BlogFormAdmin(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('name','slug','title','description')

class BlogPostFormAdmin(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ('published','blog','title','slug','content','teaser','tags')
        
    def clean(self):
        
        if self.instance.id:
            try:
                self.changed_data.index('blog')
                raise forms.ValidationError("Blog of a Blog post cannot be changed")
            except ValueError:
                None

        if not self.cleaned_data['teaser']:
            teaser = self.cleaned_data['content'][:500]
            if len(teaser)==500:
                teaser += '...'
            self.cleaned_data['teaser'] = teaser
        super(BlogPostFormAdmin,self).clean()
        return self.cleaned_data
####################################################
