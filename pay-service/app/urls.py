from django.urls import path
from .views import PaymentCreate, PaymentDetail

urlpatterns = [
    path('payments/', PaymentCreate.as_view()),
    path('payments/<int:pk>/', PaymentDetail.as_view()),
]
