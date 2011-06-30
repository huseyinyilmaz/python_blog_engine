from django import forms
from django.template.defaultfilters import slugify
from django.db.models import Q
from models import StaticPage
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
from django.utils.encoding import force_unicode

class StaticPageErrorList(forms.util.ErrorList):
    def as_ul(self):
        if not self: return u''
        return mark_safe(u'<div ><ul class="ui-state-error ui-corner-all">%s</ul></div>'
                % ''.join([u'<li class="list"><span style="float: left; margin-right: 0.3em;" class="ui-icon ui-icon-alert"></span>%s</li>' % conditional_escape(force_unicode(e)) for e in self]))

class StaticPageForm(forms.ModelForm):
    name=forms.CharField(widget=forms.TextInput(attrs={'class':'grid_7'}))
    slug=forms.CharField(widget=forms.TextInput(attrs={'class':'grid_7'}),required=False)
    title=forms.CharField(widget=forms.TextInput(attrs={'class':'grid_7'}))
    keywords=forms.CharField(widget=forms.TextInput(attrs={'class':'grid_7'}))
    description=forms.CharField(widget=forms.Textarea(attrs={'class':'grid_7','cols':'','rows':'5'}))
    content_HTML=forms.CharField(widget=forms.Textarea(attrs={'class':'grid_7','cols':'','rows':'15'}))

    class Meta:
        model = StaticPage

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        slug = slugify(slug if slug else self.cleaned_data.get('name'))
        self.cleaned_data['slug'] = slug
        # if another object with same slug exist and has different id show error
        query = Q(slug = slug)
        if self.instance.id:
            query = query & ~Q(id=self.instance.id)

        if StaticPage.objects.filter(query).exists():
            raise forms.ValidationError('There is another static with the same slug')
        return self.cleaned_data['slug']

    def clean_name(self):
        # if another object with same name exist and has different id show error
        query = Q(name = self.cleaned_data.get('name'))
        if self.instance.id:
            query = query & ~Q(id=self.instance.id)

        if StaticPage.objects.filter(query).exists():
            raise forms.ValidationError('There is another static with the same name')
        return self.cleaned_data.get('name')

    def __init__(self, *args, **kwargs):
        kwargs_new = {'error_class': StaticPageErrorList}
        kwargs_new.update(kwargs)
        super(StaticPageForm, self).__init__(*args, **kwargs_new)
