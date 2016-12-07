from models import Item, User, Fridge, Item_Fridge
from serializers import ItemSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser

class ItemList(APIView):
    """
    List all items, or create a new item.
    """
    fridge = Fridge.objects.get(pk='11')  # should get this from the session
    def get(self, request, format=None):
        items = self.fridge.items.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            new_item = Item(item_id=request.data['item_id'], item_name=request.data['item_name'], calories=request.data['calories'], unit=request.data['unit'])
            new_item.save()
            new_item_fridge = Item_Fridge(fridge_id=self.fridge, item_id=new_item, qty=request.data['qty'], unit=request.data['qty-unit'])
            new_item_fridge.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemDetail(APIView):
    """
    Retrieve, update or delete a item instance.
    """
    parser_classes = (JSONParser,)

    def get_object(self, pk):
        try:
            return Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        item = self.get_object(pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        item = self.get_object(pk)
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        item = self.get_object(pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
