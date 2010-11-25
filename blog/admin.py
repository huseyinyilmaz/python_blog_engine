from django.contrib import admin
from blog.models import Blog
from blog.models import BlogPost
from blog.models import Tag
from blog.models import BlogForm
from blog.models import BlogPostForm
class BlogAdmin(admin.ModelAdmin):
    date_hierarchy = 'creation_date'
    form = BlogForm
    list_display = ('name','slug','title','creation_date')
    #list_editable = ('slug',)
    list_select_related = True
    ordering = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ('creation_date','last_modified')
    save_on_top = True
    save_as = True
    # fieldsets = (
    #     (None, {
    #         'fields': ('name', 'title', 'description')
    #     }),
    #     # ('Advanced options', {
    #     #     'classes': ('collapse',),
    #     #     'fields': ('enable_comments', 'registration_required', 'template_name')
    #     # }),
    # )


class BlogPostAdmin(admin.ModelAdmin):
    date_hierarchy = 'creation_date'
    form = BlogPostForm
    list_display = ('title','slug','blog','creation_date','published')
    list_filter = ('blog','published')
    list_select_related = True
    ordering = ('title',)
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ('creation_date','last_modified')
    save_on_top = True
    save_as = True

class TagAdmin(admin.ModelAdmin):
    pass

admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Tag, TagAdmin)
