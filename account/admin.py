from django.contrib import admin
from .models import Profile, Item

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
	list_display = ['user', 'phone', 'photo']

class ItemAdmin(admin.ModelAdmin):
	list_display = ['title', 'owner', 'item', 'status']

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Item, ItemAdmin)