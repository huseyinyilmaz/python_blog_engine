from django import forms
from models import Blog
from models import BlogPost

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('name','slug','title','description')

class BlogPostForm(forms.ModelForm):
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
        super(BlogPostForm,self).clean()
        return self.cleaned_data
