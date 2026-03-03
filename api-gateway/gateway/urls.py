from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # Books
    path('books/', views.book_list, name='book_list'),
    path('books/add/', views.add_book, name='add_book'),
    # Customers
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/register/', views.register_customer, name='register_customer'),
    # Cart
    path('cart/<int:customer_id>/', views.view_cart, name='view_cart'),
    path('cart/<int:customer_id>/add/', views.add_to_cart, name='add_to_cart'),
    # Orders
    path('orders/', views.order_list, name='order_list'),
    path('orders/create/<int:customer_id>/', views.create_order, name='create_order'),
    # Reviews
    path('reviews/book/<int:book_id>/', views.book_reviews, name='book_reviews'),
    path('reviews/book/<int:book_id>/add/', views.add_review, name='add_review'),
    # Recommendations
    path('recommendations/', views.recommendations, name='recommendations'),
]
