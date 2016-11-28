from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Fridge
from .models import Item
from .models import Item_Fridge
from .models import Item_Store
from .models import Item_Meal
from .models import User
from .models import Store
from .models import Meal


admin.site.register(Fridge)
admin.site.register(Item)
admin.site.register(Item_Fridge)
admin.site.register(Item_Store)
admin.site.register(Item_Meal)
admin.site.register(User)
admin.site.register(Store)
admin.site.register(Meal)