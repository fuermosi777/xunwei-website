from django.contrib import admin
from api.models import *

class BusinessAdmin(admin.ModelAdmin):
    list_display = ('name', 'name2',)
    list_filter = ('city', 'postcode', 'hot_area',)
    search_fields = ['name']

# Register your models here.
admin.site.register(State)
admin.site.register(City)
admin.site.register(Tag)
admin.site.register(Postcode)
admin.site.register(Business, BusinessAdmin)
admin.site.register(Post)
admin.site.register(Post_photo)
admin.site.register(Hot_area)