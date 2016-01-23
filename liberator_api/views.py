from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import detail_route

from pprint import pprint

import json
from json import JSONEncoder

from liberator_api.models import UserMeta, Book, Shelf, ShelfItem, ShelfCache
from liberator_api import serializers

from rest_framework.authentication import SessionAuthentication, BasicAuthentication

class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = serializers.UserSerializer

    def create(self, request):
        return super(UserViewSet, self).create(request)

class EmailViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows emails to be collected
    """
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = serializers.UserSerializer

    #only allow creation - all these functions are defined to prevent the other actions
    def list(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass





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
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def list(self, request):
        if request.user.is_authenticated():
            usermeta = UserMeta.objects.get(user=request.user)
            serializer = self.serializer_class(usermeta, context={'request': request})
            return Response(serializer.data) 
        else:
            return HttpResponse(json.dumps({}), content_type="application/json")

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass

    @detail_route(methods=['post'])
    @csrf_exempt
    def addItemTolist(self, request, pk=None):
        if request.user.is_authenticated():
            usermeta = UserMeta.objects.get(user=request.user)
            book_id = int(request.POST['book_id'])
            item = Book.objects.get(pk=book_id)

            #check if the user already has a reading list
            from django.core.exceptions import ObjectDoesNotExist
            try:
                reading_list_shelf = Shelf.objects.get(creator=usermeta, title__contains="My Reading List")
            except ObjectDoesNotExist:
                reading_list_shelf = Shelf.objects.create(creator=usermeta, title="My Reading List", description="Books that I want to read.")

            #at this point, we know reading_list_shelf exists

            #find the highest order in the reading list
            highest_order = ShelfItem.objects.filter(shelf=reading_list_shelf).order_by('-order').first()
            if highest_order==None:
                highest_order = 1
            else:
                highest_order = highest_order['order']+1

            ShelfItem.objects.create(shelf=reading_list_shelf, order=highest_order, item=item)

            returnContext = {}
            returnContext['status'] = 'success'

            return HttpResponse(json.dumps(returnContext), content_type="application/json")
        else:
            returnContext = {}
            returnContext['status'] = 'error'
            returnContext['errors'] = ["User is not signed in"]

            return HttpResponse(json.dumps(returnContext), content_type="application/json")



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
    queryset = Shelf.objects.filter(status__gte=Shelf.STATUS_FRONTPAGE)
    serializer_class = serializers.ShelfSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


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

