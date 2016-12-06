from __future__ import unicode_literals

from django.db import models

# Create your models here.
# TODO: devise a global unit for conversion

class User(models.Model):
    user_id = models.CharField(max_length=200, primary_key=True)
    user_name = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    phone_no = models.CharField(max_length=20)

class Item(models.Model):
    item_id = models.CharField(max_length=200, primary_key=True)
    item_name = models.CharField(max_length=50)
    calories = models.IntegerField()
    unit = models.CharField(max_length=20)

class Fridge(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    fridge_id = models.CharField(max_length=200, primary_key=True)
    brand = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    items = models.ManyToManyField(Item, through='Item_Fridge')
    #TODO: GPS location

class Item_Fridge(models.Model):
    fridge_id = models.ForeignKey(Fridge, on_delete=models.CASCADE)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    qty = models.FloatField()
    unit = models.CharField(max_length=20)

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
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    price = models.FloatField()
    unit = models.CharField(max_length=20)
