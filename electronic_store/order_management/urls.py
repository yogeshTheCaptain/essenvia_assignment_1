from django.urls import include ,path
from rest_framework import routers
from  . import views
from .views import InventoryViewSet

router = routers.DefaultRouter()
router.register('',InventoryViewSet,basename='inventory')
router.register('',InventoryViewSet,basename='placeOrder')
router.register('',InventoryViewSet,basename='orders')

urlpatterns = [

    path('',include(router.urls)),
    path('api-auth/',include('rest_framework.urls',namespace='rest_framework'))
]