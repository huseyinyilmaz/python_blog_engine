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
