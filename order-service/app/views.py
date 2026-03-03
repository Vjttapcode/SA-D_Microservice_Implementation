from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
import requests

CART_SERVICE_URL = "http://cart-service:8000"
PAY_SERVICE_URL = "http://pay-service:8000"
SHIP_SERVICE_URL = "http://ship-service:8000"
BOOK_SERVICE_URL = "http://book-service:8000"


class OrderCreate(APIView):
    def post(self, request):
        customer_id = request.data.get("customer_id")
        shipping_address = request.data.get("shipping_address", "")
        payment_method = request.data.get("payment_method", "cash")

        # Get cart items from cart-service
        cart_items = []
        try:
            r = requests.get(f"{CART_SERVICE_URL}/api/carts/{customer_id}/")
            if r.status_code == 200:
                cart_data = r.json()
                cart_items = cart_data.get("items", [])
        except requests.exceptions.ConnectionError:
            pass

        if not cart_items:
            return Response({"error": "Cart is empty or not found"}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate total by fetching book prices
        total = 0
        order_items_data = []
        for item in cart_items:
            book_price = 0
            try:
                br = requests.get(f"{BOOK_SERVICE_URL}/api/books/{item['book_id']}/")
                if br.status_code == 200:
                    book_price = float(br.json().get("price", 0))
            except requests.exceptions.ConnectionError:
                pass
            item_total = book_price * item["quantity"]
            total += item_total
            order_items_data.append({
                "book_id": item["book_id"],
                "quantity": item["quantity"],
                "price": book_price
            })

        # Create order
        order = Order.objects.create(
            customer_id=customer_id,
            total_amount=total,
            shipping_address=shipping_address,
            payment_method=payment_method,
            status='pending'
        )

        # Create order items
        for item_data in order_items_data:
            OrderItem.objects.create(order=order, **item_data)

        # Trigger payment via pay-service
        try:
            requests.post(
                f"{PAY_SERVICE_URL}/api/payments/",
                json={
                    "order_id": order.id,
                    "amount": str(total),
                    "method": payment_method,
                }
            )
        except requests.exceptions.ConnectionError:
            pass

        # Trigger shipping via ship-service
        try:
            requests.post(
                f"{SHIP_SERVICE_URL}/api/shipments/",
                json={
                    "order_id": order.id,
                    "address": shipping_address,
                }
            )
        except requests.exceptions.ConnectionError:
            pass

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderList(APIView):
    def get(self, request):
        customer_id = request.query_params.get("customer_id")
        if customer_id:
            orders = Order.objects.filter(customer_id=customer_id)
        else:
            orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class OrderDetail(APIView):
    def get(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        order.status = request.data.get("status", order.status)
        order.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)
