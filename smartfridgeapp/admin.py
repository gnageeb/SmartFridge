from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Fridge
from .models import Item
from .models import Item_Fridge
from .models import Item_Store
from .models import Item_Meal
from .models import Fridge_Day_Calories
from .models import Store
from .models import Meal,Basket,Basket_Item


admin.site.register(Fridge)
admin.site.register(Item)
admin.site.register(Item_Fridge)
admin.site.register(Fridge_Day_Calories)
admin.site.register(Basket)
admin.site.register(Basket_Item)
admin.site.register(Item_Store)
admin.site.register(Item_Meal)
admin.site.register(Store)
admin.site.register(Meal)