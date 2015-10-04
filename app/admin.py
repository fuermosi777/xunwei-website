from django.contrib import admin
from app.models import *


class RestaurantAdmin(admin.ModelAdmin):
	list_display = ('id','name', 'name2','city','postcode','display_subcategory','phone', 'photo_image')
	search_fields = ('name','name2')
	list_filter = ('city','city__state')
	filter_horizontal = ('subcategory',)

class TimeAdmin(admin.ModelAdmin):
	filter_horizontal = ('restaurant',)

class SubcategoryAdmin(admin.ModelAdmin):
	list_display = ('id','name')
	# filter_horizontal = ('restaurant',)

# Register your models here.
admin.site.register(Restaurant,RestaurantAdmin)
admin.site.register(Status)
admin.site.register(Review)
admin.site.register(Category)
admin.site.register(Subcategory,SubcategoryAdmin)
admin.site.register(City)
admin.site.register(Postcode)
admin.site.register(State)
admin.site.register(Review_photo)
admin.site.register(UserProfile)
admin.site.register(Journal)
admin.site.register(Ad)