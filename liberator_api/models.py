from django.db import models
from django.contrib.auth.models import User

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


class ShelfCache(models.Model):
	user = models.ForeignKey(User)
	jsonCache = models.TextField()

