from django.db import models
from django.contrib.auth.models import User

class ShelfCache(models.Model):
	user = models.ForeignKey(User)
	jsonCache = models.TextField()

