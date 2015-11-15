from django.contrib import admin
from liberator_api.models import ShelfCache, UserMeta

# Register your models here.
@admin.register(UserMeta)
class UserMetaAdmin(admin.ModelAdmin):
	pass

@admin.register(ShelfCache)
class ShelfCacheAdmin(admin.ModelAdmin):
	pass
