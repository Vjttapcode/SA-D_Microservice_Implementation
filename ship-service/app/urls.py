from django.urls import path
from .views import ShipmentCreate, ShipmentDetail

urlpatterns = [
    path('shipments/', ShipmentCreate.as_view()),
    path('shipments/<int:pk>/', ShipmentDetail.as_view()),
]
