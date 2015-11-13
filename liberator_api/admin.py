from django.contrib import admin
from liberator_api.models import ShelfCache

# Register your models here.
@admin.register(ShelfCache)
class ShelfCacheAdmin(admin.ModelAdmin):
	pass
