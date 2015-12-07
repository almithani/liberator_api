from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone

#
class UserMeta(models.Model):
	user = models.ForeignKey(User)
	avatar = models.ImageField(upload_to='user_avatars/', blank=True)
	displayName = models.CharField(max_length=50, blank=True)
	tagline = models.CharField(max_length=100, blank=True)
	description = models.TextField(blank=True)

	def __unicode__(self):
		return self.displayName


class Book(models.Model):
	title = models.CharField(max_length=600)
	author = models.CharField(max_length=50)
	description = models.TextField(blank=True)
	cover = models.ImageField(upload_to='covers/', blank=True)
	ISBN = models.CharField(max_length=14, blank=True)

	def __unicode__(self):
		return self.title + ' - ' + self.author


class Shelf(models.Model):
	title = models.CharField(max_length=200)
	creator = models.ForeignKey(UserMeta)
	description = models.TextField(blank=True)
	items = models.ManyToManyField(Book, through='ShelfItem')
	date_added = models.DateTimeField(default=timezone.now)

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

