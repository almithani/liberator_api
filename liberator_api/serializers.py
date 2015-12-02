from django.contrib.auth.models import User, Group

from rest_framework import serializers

from liberator_api.models import UserMeta, Book, ShelfCache

# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'username', 'email')

class UserMetaSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	avatar = serializers.ImageField()

	class Meta:
		model = UserMeta
		fields = '__all__'
		depth = 1

class GroupSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Group
		fields = ('url', 'name')

class BookSerializer(serializers.ModelSerializer):
	class Meta:
		model = Book
		fields = '__all__'

class ShelfCacheSerializer(serializers.ModelSerializer):
	class Meta:
		model = ShelfCache
		fields = ('id', 'url', 'user', 'jsonCache')