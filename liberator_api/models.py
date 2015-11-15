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


class ShelfCache(models.Model):
	user = models.ForeignKey(User)
	jsonCache = models.TextField()

