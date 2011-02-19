from django.db import models
class MenuItem(models.Model):
    """
    MenuItems that used to create menu
    """
    name = models.CharField('Name of the MenuItem',max_length=255,unique=True)
    display = models.CharField('Display of the MenuItem',max_length=255,unique=True)
    url = models.CharField('URL of menuitem',max_length=255)
    extra_property = models.CharField(max_length=255,blank=True)
    order = models.IntegerField()
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.name
    def __unicode__(self):
        return unicode(str(self))

def get_menu_items():
    fields = ('order','url','display','extra_property')
    mi = MenuItem.objects.filter(is_active=True).order_by('order','-id').values_list(*fields)
    return (dict( zip(fields,row) ) for row in mi)
