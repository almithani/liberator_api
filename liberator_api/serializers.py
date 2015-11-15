from django.contrib.auth.models import User, Group

from rest_framework import serializers

from liberator_api.models import UserMeta, ShelfCache

# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'username', 'email')

class UserMetaSerializer(serializers.ModelSerializer):
	user = UserSerializer()

	class Meta:
		model = UserMeta
		fields = '__all__'
		depth = 1

class GroupSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Group
		fields = ('url', 'name')

class ShelfCacheSerializer(serializers.ModelSerializer):
	class Meta:
		model = ShelfCache
		fields = ('id', 'url', 'user', 'jsonCache')