from django.contrib import admin

from comment.models import Comment

class CommentAdmin(admin.ModelAdmin):
    date_hierarchy = 'creation_date'
    list_display = ('name','email','website','creation_date','blogpost')
    list_select_related = True
    ordering = ('-creation_date',)
    readonly_fields = ('creation_date','last_modified')
    save_on_top = True
    save_as = True
    search_fields = ['name','email']

admin.site.register(Comment, CommentAdmin)
