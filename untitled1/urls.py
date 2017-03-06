"""untitled1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from smartfridgeapp import views
from rest_framework.urlpatterns import format_suffix_patterns

router = routers.DefaultRouter()
#router.register(r'items', views.ItemViewSet)

urlpatterns = [
    #url(r'^smartfridgeapp/', include('smartfridgeapp.urls')),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),
    url(r'^items/(?P<pk>[0-9a-z-]+)/$', views.ItemDetail.as_view()),
    url(r'^items/(?P<item_id>[0-9a-z-]+)/stores/$', views.GetStores.as_view()),
    url(r'^users/fridge/items/$', views.ItemList.as_view()),
    url(r'^users/fridge/items/consume$', views.ConsumeItem.as_view()),
    url(r'^users/login/$', views.AccountLogin.as_view()),
    url(r'^users/register/$', views.AccountRegister.as_view()),
    url(r'^users/fridge/$', views.FridgeDetail.as_view()),
    url(r'^users/fridge/setitemthreshold/$', views.SetItemThreshold.as_view()),
    url(r'^users/fridge/totalcalories/$', views.ConsumedCalories.as_view()),
    url(r'^users/basket/$', views.ListBasketItems.as_view()),
]

#urlpatterns = format_suffix_patterns(urlpatterns)