"""order_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url, include
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from orders.views import OrderViewset, CartItemViewset, ProductViewset


schema_view = get_schema_view(
   openapi.Info(
      title="Order API",
      default_version='v1',
   )
)


router = routers.DefaultRouter()
router.register(r"orders", OrderViewset, basename="order")
orders_router = routers.NestedSimpleRouter(router, r"orders", lookup="order")
orders_router.register(r"cart-items", CartItemViewset, basename="order-cart-items")

router.register(r"products", ProductViewset, basename="order")

urlpatterns = [
    url(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-redoc'),
    url(r"^", include(router.urls)),
    url(r"^", include(orders_router.urls)),
]