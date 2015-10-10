from django.contrib import admin
from api.models import *

class BusinessAdmin(admin.ModelAdmin):
    list_display = ('name', 'name2',)
    list_filter = ('city', 'postcode', 'hot_area',)
    search_fields = ['name', 'name2']

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'source',)
    list_filter = ('is_approved', 'business__hot_area')
    search_fields = ['title']

# Register your models here.
admin.site.register(State)
admin.site.register(City)
admin.site.register(Tag)
admin.site.register(Postcode)
admin.site.register(Business, BusinessAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Post_photo)
admin.site.register(Hot_area)