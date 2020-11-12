from django.contrib.auth.models import User, Group

from rest_framework import serializers

from liberator_api.models import UserMeta, Book, Shelf, ShelfItem, ShelfCache

# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'username', 'email', 'password')

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
		fields = ('title', 'author', 'description', 'cover', 'ISBN')


class ShelfItemSerializer(serializers.ModelSerializer):

	id = serializers.IntegerField(source='item.id')
	title = serializers.CharField(source='item.title', max_length=600 )
	author = serializers.CharField(source='item.author', max_length=50 )
	description = serializers.CharField(source='item.description', allow_blank=True, required=False, style={'base_template': 'textarea.html'})
	cover = serializers.ImageField(source='item.cover', required=False)
	ISBN = serializers.CharField(source='item.ISBN', allow_blank=True, label='ISBN', max_length=14, required=False)
	amazon_link = serializers.CharField(source='item.amazon_link', allow_blank=True, max_length=2083, required=False)

	class Meta:
		model = ShelfItem
		fields = ('id', 'title', 'author', 'description', 'cover', 'ISBN', 'amazon_link', 'quote', 'order')


class ShelfSerializer(serializers.ModelSerializer):

	items = ShelfItemSerializer(source='shelfitem_set', many=True, read_only=True)

	class Meta:
		model = Shelf
		fields = ('id', 'title', 'creator', 'description', 'items' )
		depth = 1


class ShelfCacheSerializer(serializers.ModelSerializer):
	class Meta:
		model = ShelfCache
		fields = ('id', 'url', 'user', 'jsonCache')