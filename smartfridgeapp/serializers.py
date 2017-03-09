from models import Item, Fridge, Fridge_Day_Calories, Item_Fridge, Basket_Item, Item_Store
from rest_framework import serializers
from django.contrib.auth.models import User



class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = ('item_id', 'item_name', 'calories')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password',"email")


class FridgeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Fridge
        fields = ('brand','model')


class FridgeDayCaloriesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Fridge_Day_Calories
        fields = ('calories', 'date')


class ItemFridgeSerializer(serializers.HyperlinkedModelSerializer):
    item_name = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Item_Fridge
        fields = ("item_id","item_name","qty","unit","threshold","calories")


class BasketItemSerializer(serializers.HyperlinkedModelSerializer):
    item_name = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Basket_Item
        fields = ("item_id","item_name","qty","unit")


class ItemStoreSerializer(serializers.HyperlinkedModelSerializer):
    store_name = serializers.PrimaryKeyRelatedField(read_only=True)
    item_name = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Item_Store
        fields = ("store_name","item_name","unit","price","store_id","item_id")