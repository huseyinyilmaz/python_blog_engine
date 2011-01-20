from django.contrib import admin

from blog.models import Blog
from blog.models import BlogPost
from blog.models import Tag

from blog.forms import BlogFormAdmin
from blog.forms import BlogPostFormAdmin

#########################################
class BlogAdmin(admin.ModelAdmin):
    date_hierarchy = 'creation_date'
    form = BlogFormAdmin
    list_display = ('name','slug','title','creation_date')
    list_select_related = True
    ordering = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ('creation_date','last_modified')
    save_on_top = True
    save_as = True
    search_fields = ['name','title']

class BlogPostAdmin(admin.ModelAdmin):
    date_hierarchy = 'creation_date'
    form = BlogPostFormAdmin
    list_display = ('title','slug','blog','creation_date','published')
    list_filter = ('blog','published')
    list_select_related = True
    ordering = ('title',)
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ('creation_date','last_modified')
    save_on_top = True
    save_as = True
    search_fields = ['title']
    # def save_model(self, request, obj, form, change):
    #     obj.teaser_HTML = obj.teaser
    #     obj.content_HTML = obj.content
    #     obj.save()

class TagAdmin(admin.ModelAdmin):
    pass

admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Tag, TagAdmin)
