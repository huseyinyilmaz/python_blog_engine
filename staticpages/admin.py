from django.contrib import admin
from staticpages.models import StaticPage

class StaticPageAdmin(admin.ModelAdmin):
    date_hierarchy = 'creation_date'
    pass
admin.site.register(StaticPage, StaticPageAdmin)
