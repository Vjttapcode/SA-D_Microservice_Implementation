from django.urls import path
from .views import RecommendBooks, RecommendForCustomer

urlpatterns = [
    path('recommendations/', RecommendBooks.as_view()),
    path('recommendations/customer/<int:customer_id>/', RecommendForCustomer.as_view()),
]
