from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import list_route, detail_route

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



class SearchViewSet(viewsets.ViewSet):
    """
    API endpoint that handles searching for new books 
    """ 

    #serializer_class = 
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def create(self, request):

        import bottlenose
        from lxml import objectify
        import firstsite.settings as settings

        # get results from amazon
        searchString = request.POST['book']
        amazon = bottlenose.Amazon(settings.AWS_ACCESS, settings.AWS_SECRET, settings.AWS_ASSOC)
        response = amazon.ItemSearch(Keywords=searchString, SearchIndex="Books", ResponseGroup="ItemAttributes, Images")
        response_object = objectify.fromstring(response)

        #grab the values we actually need and stuff them into a dict
        response_dict = {}
        response_dict['results'] = []

        for item in response_object.Items.Item:
            item_dict = {}
            item_dict['title'] = str(item.ItemAttributes.Title)
            item_dict['author'] = str(item.ItemAttributes.Author)
            item_dict['image'] = str(item.LargeImage.URL)
            item_dict['url'] = str(item.DetailPageURL)

            response_dict['results'].append(item_dict)


        return HttpResponse(json.dumps(response_dict), content_type="application/json")



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

            reading_list_shelf = usermeta.getReadingList().first()

            #find the highest order in the reading list
            highest_order = ShelfItem.objects.filter(shelf=reading_list_shelf).order_by('-order').first()
            if highest_order==None:
                highest_order = 1
            else:
                highest_order = highest_order.order+1

            ShelfItem.objects.create(shelf=reading_list_shelf, order=highest_order, item=item)

            returnContext = {}
            returnContext['status'] = 'success'

            return HttpResponse(json.dumps(returnContext), content_type="application/json")
        else:
            returnContext = {}
            returnContext['status'] = 'error'
            returnContext['errors'] = ["User is not signed in"]

            return HttpResponse(json.dumps(returnContext), content_type="application/json")

    @list_route(methods=['get'])
    @csrf_exempt
    def readingList(self, request):
        if request.user.is_authenticated():
            usermeta = UserMeta.objects.get(user=request.user)  
            self.queryset = usermeta.getReadingList()
            self.serializer_class = serializers.ShelfSerializer
            #serializer = serializers.ShelfSerializer(queryset)

            #return Response(serializer.data)
            return viewsets.ModelViewSet.list(self, request)

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
    queryset = Shelf.objects.all()
    serializer_class = serializers.ShelfSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def list(self, request):
        self.queryset = Shelf.objects.filter(status__gte=Shelf.STATUS_FRONTPAGE)
        return super(ShelfViewSet, self).list(request)

    def retrieve(self, request, pk=None):
        self.queryset = Shelf.objects.filter(pk__exact=pk, status__gte=Shelf.STATUS_PUBLIC)
        return super(ShelfViewSet, self).retrieve(request)

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

    def retrieve(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        from rest_framework.renderers import JSONRenderer
        from django.http import HttpResponse
        
        json = JSONRenderer().render(serializer.data)
        return HttpResponse(json, content_type="application/json")

