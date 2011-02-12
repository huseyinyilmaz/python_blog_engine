from django.contrib import admin
from models import StaticPage

class StaticPageAdmin(admin.ModelAdmin):
    date_hierarchy = 'creation_date'
    pass
admin.site.register(StaticPage, StaticPageAdmin)
