from __future__ import unicode_literals

from django.db import models

# Create your models here.
# TODO: devise a global unit for conversion

from django.contrib.auth.models import User


class Item(models.Model):
    item_id = models.CharField(max_length=200, primary_key=True)
    item_name = models.CharField(max_length=50)
    calories = models.IntegerField(default=0)



class Fridge(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    fridge_id = models.CharField(max_length=200, primary_key=True)
    brand = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    items = models.ManyToManyField(Item, through='Item_Fridge')
    #TODO: GPS location

class Item_Fridge(models.Model):
    fridge = models.ForeignKey(Fridge, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    qty = models.FloatField(default=0)
    threshold = models.FloatField(default=0)
    unit = models.CharField(max_length=20)

    @property
    def item_name(self):
        return self.item.item_name

    @property
    def calories(self):
        return self.item.calories


class Fridge_Day_Calories(models.Model):
    fridge_id = models.ForeignKey(Fridge, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    calories = models.IntegerField(default=0)


class Meal(models.Model):
    meal_id = models.CharField(max_length=200, primary_key=True)
    meal_name = models.CharField(max_length=50)
    meal_recipe = models.CharField(max_length=1000)
    items = models.ManyToManyField(Item, through='Item_Meal')


class Item_Meal(models.Model):
    meal_id = models.ForeignKey(Meal, on_delete=models.CASCADE)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    qty = models.FloatField()
    unit = models.CharField(max_length=20)


class Store(models.Model):
    store_id = models.CharField(max_length=200, primary_key=True)
    store_name = models.CharField(max_length=50)
    phone_no = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    website = models.URLField()
    products = models.ManyToManyField(Item, through='Item_Store')
    # TODO: GPS location
    # TODO: get products by an API


class Item_Store(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    unit = models.CharField(max_length=20)

    @property
    def store_name(self):
        return self.store.store_name


    @property
    def item_name(self):
        return self.item.item_name


class Basket(models.Model):
    basket_id = models.CharField(max_length=200, primary_key=True)
    shopper = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, through='Basket_Item')


class Basket_Item(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    qty = models.FloatField(default=0)
    unit = models.CharField(max_length=20)

    @property
    def item_name(self):
        return self.item.item_name