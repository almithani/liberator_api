from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response

from pprint import pprint

import json
from json import JSONEncoder

from liberator_api.models import UserMeta, Book, Shelf, ShelfItem, ShelfCache
from liberator_api import serializers


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = serializers.UserSerializer

    def create(self, request):
        return super(UserViewSet, self).create(request)


class UserMetaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = (permissions.AllowAny,)
    queryset = UserMeta.objects.all()
    serializer_class = serializers.UserMetaSerializer

    #def retrieve(self, request, pk=None):
    #    usermeta = UserMeta.objects.get(user__id=pk)
    #    serializer = self.serializer_class(usermeta)
    #    return Response(serializer.data)  



class CurrentUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows actions on currently logged in user
    """ 

    serializer_class = serializers.UserMetaSerializer
    permission_classes = (permissions.AllowAny,)

    def list(self, request):
        if request.user.is_authenticated():
            usermeta = UserMeta.objects.get(user=request.user)
            serializer = self.serializer_class(usermeta, context={'request': request})
            return Response(serializer.data) 
        else:
            return HttpResponse(json.dumps({}), content_type="application/json")


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows books to be viewed or edited.
    """
    queryset = Book.objects.all()
    serializer_class = serializers.BookSerializer


class ShelfViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows shelfs to be viewed or edited.
    """
    queryset = Shelf.objects.all()
    serializer_class = serializers.ShelfSerializer

class ShelfItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows shelf items to be viewed or edited.
    """
    queryset = ShelfItem.objects.all()
    serializer_class = serializers.ShelfItemSerializer


class BoardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows boards to be viewed or edited.
    """
    permission_classes = (permissions.AllowAny,)
    queryset = ShelfCache.objects.all()
    serializer_class = serializers.ShelfCacheSerializer  

    def retreve(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        from rest_framework.renderers import JSONRenderer
        from django.http import HttpResponse
        
        json = JSONRenderer().render(serializer.data)
        return HttpResponse(json, content_type="application/json")

