from models import Item, Fridge, Item_Fridge, Fridge_Day_Calories, Basket, Basket_Item, Item_Store, Store
from serializers import ItemSerializer, UserSerializer, ItemStoreSerializer, FridgeSerializer,FridgeDayCaloriesSerializer,BasketItemSerializer, ItemFridgeSerializer
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
import uuid, datetime


class ItemList(APIView):
    """
    List all items, or create a new item.
    """
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        fridge = Fridge.objects.get(owner=request.user)
        fridge_items = Item_Fridge.objects.filter(fridge=fridge)
        serializer = ItemFridgeSerializer(fridge_items, many=True)
        return Response(serializer.data)

    def post(self,request):
        owner = request.user
        fridge = Fridge.objects.get(owner=owner)
        item_id = request.data["item_id"]
        item_name = request.data["item_name"]
        calories = request.data["calories"]
        unit = request.data["unit"]
        qty = request.data["qty"]
        item, created = Item.objects.get_or_create(item_id=item_id)
        basket = Basket.objects.get(shopper=owner)
        item.item_name = item_name
        item.calories = calories
        try:
            basket_item = Basket_Item.objects.get(item=item, basket=basket)
        except Basket_Item.DoesNotExist:
            basket_item = None
        if basket_item is not None:
            basket_item.qty -= qty
            basket_item.save()
            if basket_item.qty <= 0:
                basket_item.delete()

        item_fridge, created = Item_Fridge.objects.get_or_create(item=item, fridge=fridge)
        item_fridge.qty += qty
        item_fridge.unit = unit
        item_fridge.save()
        item.save()
        if not created:
            return Response(status=status.HTTP_302_FOUND)

        return Response(status=status.HTTP_201_CREATED)


class ItemDetail(APIView):
    """
    Retrieve, update or delete a item instance.
    """
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
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

    # TODO: delete item form fridge
    def delete(self, request, pk, format=None):
        item = self.get_object(pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AccountLogin(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (AllowAny,)
    def post(self,request):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        serializer = UserSerializer(user, data=request.data)

        if serializer.is_valid() and not user == None:
            # the password verified for the user
            if user.is_active:
                login(request, user)
                return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class AccountRegister(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (AllowAny,)

    def post(self,request):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = User.objects.create_user(request.data['username'],
                                            request.data['email'],
                                            request.data['password'])
            #assign fridge to the user
            new_fridge = Fridge(owner=user,fridge_id=uuid.uuid4())
            new_fridge.save()
            # assign fridge to the user
            new_basket = Basket(shopper=user, basket_id=uuid.uuid4())
            new_basket.save()
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class FridgeDetail(APIView):
    """
       Retrieve, update a fridge instance.
       """
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)

    def get_object(self,owner):
        try:
            return Fridge.objects.get(owner=owner)
        except Fridge.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        owner = request.user
        fridge = self.get_object(owner)
        serializer = FridgeSerializer(fridge)
        return Response(serializer.data)

    def post(self, request, format=None):
        owner = request.user
        fridge = self.get_object(owner)
        serializer = FridgeSerializer(fridge, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConsumeItem(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)

    def post(self, request):
        owner = request.user
        fridge = Fridge.objects.get(owner=owner)
        item_id = request.data["item_id"]
        try:
            item = fridge.items.get(item_id=item_id)
            fridge_item = Item_Fridge.objects.get(fridge=fridge, item=item)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        fridge_day_calories, _ = Fridge_Day_Calories.objects.get_or_create(fridge_id=fridge,date=datetime.date.today())
        fridge_day_calories.calories += item.calories * request.data["qty"]
        fridge_day_calories.save()
        if fridge_item.qty >= request.data["qty"]:
            fridge_item.qty -= request.data["qty"]
            if fridge_item.qty < fridge_item.threshold:
                basket = Basket.objects.get(shopper=owner)
                basket_item, _ = Basket_Item.objects.get_or_create(basket=basket, item=item)
                basket_item.qty = fridge_item.threshold - fridge_item.qty
                basket_item.unit = fridge_item.unit
                basket.save()
                basket_item.save()
            if fridge_item.qty <= 0:
                fridge_item.delete()
            else:
                fridge_item.save()
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_202_ACCEPTED)


class ConsumedCalories(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        owner = request.user
        fridge = Fridge.objects.get(owner=owner)
        date = datetime.date.today()
        fdc, _ = Fridge_Day_Calories.objects.get_or_create(fridge_id=fridge, date=date)
        serializer = FridgeDayCaloriesSerializer(fdc)
        return Response(serializer.data)

    #TODO:post for getting accumlative calories and days' total calories in a date range


class SetItemThreshold(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)

    def post(self,request):
        owner = request.user
        fridge = Fridge.objects.get(owner=owner)
        item_id = request.data["item_id"]
        try:
            item = fridge.items.get(item_id=item_id)
            fridge_item = Item_Fridge.objects.get(fridge=fridge, item=item)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        fridge_item.threshold = request.data["threshold"]
        fridge_item.save()

        return Response(status=status.HTTP_202_ACCEPTED)


class ListBasketItems(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)

    def get(self,request):
        owner = request.user
        basket = Basket.objects.get(shopper=owner)
        basket_items = Basket_Item.objects.filter(basket=basket)
        serializer = BasketItemSerializer(basket_items, many=True)
        return Response(serializer.data)


class GetStores(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)

    def get(self,request,item_id):
        item = Item.objects.get(item_id=item_id)
        item_stores = Item_Store.objects.filter(item_id=item)
        serializer = ItemStoreSerializer(item_stores, many= True)
        return Response(serializer.data)
