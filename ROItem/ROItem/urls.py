"""ROItem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from api_test.views import UserViewSet, testApi
from item.views import query_item, create_item, change_item, text_Item, download_page
from login.views import index, login, logout

router = routers.DefaultRouter()  # API測試
router.register(r'users', UserViewSet)  # API測試

urlpatterns = [
    path("admin/", admin.site.urls),
    path('index/', index),
    path('accounts/login/', login),
    path("accounts/logout/", logout),
    path('', include(router.urls)),  # API測試
    path('api-auth/', include('rest_framework.urls')),  # API測試
    path('testApi/', testApi, name="testApi"),  # API測試

    path("queryItem/", query_item, name='query_item'),
    path("createitem/", create_item, name='create_item'),
    path("changeItem/", change_item, name='change_item'),
    path("textItem/", text_Item, name='text_Item'),
    path("download_page/", download_page, name='download_page')
]
