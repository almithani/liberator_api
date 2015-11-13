from django.contrib.auth.models import User, Group

from rest_framework import serializers

from liberator_api.models import ShelfCache

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'email', 'is_staff')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class ShelfCacheSerializer(serializers.ModelSerializer):
	class Meta:
		model = ShelfCache
		fields = ('id', 'url', 'user', 'jsonCache')