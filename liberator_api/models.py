from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone

#
class UserMeta(models.Model):
	READING_LIST_TITLE = "My Reading List"

	user = models.ForeignKey(User)
	avatar = models.ImageField(upload_to='user_avatars/', blank=True)
	displayName = models.CharField(max_length=50, blank=True)
	tagline = models.CharField(max_length=100, blank=True)
	description = models.TextField(blank=True)

	def getReadingList(self):
		from django.core.exceptions import ObjectDoesNotExist
		try:
			reading_list_shelf = Shelf.objects.filter(creator=self, title__contains=self.READING_LIST_TITLE)
		except ObjectDoesNotExist: 
			Shelf.objects.create(creator=self, title=self.READING_LIST_TITLE, description="Books that I want to read.")
			reading_list_shelf = Shelf.objects.filter(creator=self, title__contains=self.READING_LIST_TITLE)

		return reading_list_shelf

	def __unicode__(self):
		return self.displayName


class Book(models.Model):
	title = models.CharField(max_length=600)
	author = models.CharField(max_length=50)
	description = models.TextField(blank=True)
	cover = models.ImageField(upload_to='covers/', blank=True)
	ISBN = models.CharField(max_length=14, blank=True)
	amazon_link = models.CharField(max_length=2083, blank=True)

	def __unicode__(self):
		return self.title + ' - ' + self.author


class Shelf(models.Model):
	STATUS_PRIVATE = 0
	STATUS_PUBLIC = 1
	STATUS_FRONTPAGE = 2

	STATUS_ENUM = (
		(STATUS_PRIVATE, 'PRIVATE'),
		(STATUS_PUBLIC, 'PUBLIC'),
		(STATUS_FRONTPAGE, 'FRONTPAGE')
	)

	title = models.CharField(max_length=200)
	creator = models.ForeignKey(UserMeta)
	description = models.TextField(blank=True)
	items = models.ManyToManyField(Book, through='ShelfItem')
	date_added = models.DateTimeField(default=timezone.now)
	status = models.IntegerField(choices=STATUS_ENUM, default=STATUS_PUBLIC)

	def __unicode__(self):
		return self.title + ' - ' + self.creator.displayName

	class Meta: 
		ordering = ['-date_added']


class ShelfItem(models.Model):
	shelf = models.ForeignKey(Shelf)
	item = models.ForeignKey(Book)
	quote = models.CharField(max_length=140, blank=True)
	order = models.IntegerField(blank=True, default=1)

	def __unicode__(self):
		return self.shelf.title + ' - ' + self.item.title

	class Meta: 
		ordering = ['order']


class ShelfCache(models.Model):
	user = models.ForeignKey(User)
	jsonCache = models.TextField()

