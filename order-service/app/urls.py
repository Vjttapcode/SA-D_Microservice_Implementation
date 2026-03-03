from django.urls import path
from .views import OrderCreate, OrderList, OrderDetail

urlpatterns = [
    path('orders/', OrderCreate.as_view()),
    path('orders/list/', OrderList.as_view()),
    path('orders/<int:pk>/', OrderDetail.as_view()),
]
