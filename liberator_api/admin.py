from django.contrib import admin
from liberator_api.models import ShelfCache, UserMeta, Book, Shelf, ShelfItem

# Register your models here.
@admin.register(UserMeta)
class UserMetaAdmin(admin.ModelAdmin):
	pass

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	pass

@admin.register(Shelf)
class ShelfAdmin(admin.ModelAdmin):
	list_display = ('pk', 'creator', 'title', 'date_added')
	pass

@admin.register(ShelfItem)
class ShelfItemAdmin(admin.ModelAdmin):
	pass

@admin.register(ShelfCache)
class ShelfCacheAdmin(admin.ModelAdmin):
	pass
