from django.contrib import admin
from menu.models import MenuItem

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('id','order','name','url','is_active')
    list_display_links = ('id','name')
    ordering = ['order','is_active','id']
admin.site.register(MenuItem,MenuItemAdmin)
