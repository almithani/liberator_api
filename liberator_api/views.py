from django.shortcuts import render
from django.contrib.auth.models import User, Group

from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from liberator_api.models import ShelfCache
from liberator_api.serializers import UserSerializer, GroupSerializer, ShelfCacheSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = (AllowAny,)
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    def create(self, request):
        return super(UserViewSet, self).create(request)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class BoardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows boards to be viewed or edited.
    """
    permission_classes = (AllowAny,)
    queryset = ShelfCache.objects.all()
    serializer_class = ShelfCacheSerializer  

    def retreve(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        from rest_framework.renderers import JSONRenderer
        from django.http import HttpResponse
        
        json = JSONRenderer().render(serializer.data)
        return HttpResponse(json, content_type="application/json")

