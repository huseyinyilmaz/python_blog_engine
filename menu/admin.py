from django.contrib import admin

from menu.models import Menu

from menu.models import MenuForm


class MenuAdmin(admin.ModelAdmin):
#    date_hierarchy = 'creation_date'
    form = MenuForm
    list_display = ('title','itemtype','order','enabled')
    list_select_related = True
    ordering = ('title',)
    save_on_top = True
    save_as = True


admin.site.register(Menu, MenuAdmin)
