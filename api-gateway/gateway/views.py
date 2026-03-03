from django.shortcuts import render
from django.http import JsonResponse
import requests

# Service URLs (Docker service names)
CUSTOMER_SERVICE_URL = "http://customer-service:8000"
STAFF_SERVICE_URL = "http://staff-service:8000"
BOOK_SERVICE_URL = "http://book-service:8000"
CART_SERVICE_URL = "http://cart-service:8000"
ORDER_SERVICE_URL = "http://order-service:8000"
PAY_SERVICE_URL = "http://pay-service:8000"
SHIP_SERVICE_URL = "http://ship-service:8000"
CATALOG_SERVICE_URL = "http://catalog-service:8000"
COMMENT_RATE_SERVICE_URL = "http://comment-rate-service:8000"
RECOMMENDER_SERVICE_URL = "http://recommender-ai-service:8000"


def index(request):
    return render(request, "index.html")


# ===== Book Management (Staff) =====
def book_list(request):
    books = []
    try:
        r = requests.get(f"{BOOK_SERVICE_URL}/api/books/")
        if r.status_code == 200:
            books = r.json()
    except requests.exceptions.ConnectionError:
        pass
    return render(request, "books.html", {"books": books})


def add_book(request):
    if request.method == "POST":
        data = {
            "title": request.POST.get("title"),
            "author": request.POST.get("author"),
            "price": request.POST.get("price"),
            "stock": request.POST.get("stock"),
            "isbn": request.POST.get("isbn", ""),
        }
        try:
            requests.post(f"{BOOK_SERVICE_URL}/api/books/", json=data)
        except requests.exceptions.ConnectionError:
            pass
    return render(request, "add_book.html")


# ===== Customer Management =====
def customer_list(request):
    customers = []
    try:
        r = requests.get(f"{CUSTOMER_SERVICE_URL}/api/customers/")
        if r.status_code == 200:
            customers = r.json()
    except requests.exceptions.ConnectionError:
        pass
    return render(request, "customers.html", {"customers": customers})


def register_customer(request):
    if request.method == "POST":
        data = {
            "name": request.POST.get("name"),
            "email": request.POST.get("email"),
        }
        try:
            requests.post(f"{CUSTOMER_SERVICE_URL}/api/customers/", json=data)
        except requests.exceptions.ConnectionError:
            pass
    return render(request, "register_customer.html")


# ===== Cart =====
def view_cart(request, customer_id):
    cart = {}
    try:
        r = requests.get(f"{CART_SERVICE_URL}/api/carts/{customer_id}/")
        if r.status_code == 200:
            cart = r.json()
    except requests.exceptions.ConnectionError:
        pass
    return render(request, "cart.html", {"cart": cart, "customer_id": customer_id})


def add_to_cart(request, customer_id):
    if request.method == "POST":
        # Get cart for customer
        try:
            r = requests.get(f"{CART_SERVICE_URL}/api/carts/{customer_id}/")
            if r.status_code == 200:
                cart = r.json()
                data = {
                    "cart": cart["id"],
                    "book_id": int(request.POST.get("book_id")),
                    "quantity": int(request.POST.get("quantity", 1)),
                }
                requests.post(f"{CART_SERVICE_URL}/api/cart-items/", json=data)
        except requests.exceptions.ConnectionError:
            pass
    # Get books for the form
    books = []
    try:
        r = requests.get(f"{BOOK_SERVICE_URL}/api/books/")
        if r.status_code == 200:
            books = r.json()
    except requests.exceptions.ConnectionError:
        pass
    return render(request, "add_to_cart.html", {"books": books, "customer_id": customer_id})


# ===== Orders =====
def create_order(request, customer_id):
    if request.method == "POST":
        data = {
            "customer_id": customer_id,
            "shipping_address": request.POST.get("address", ""),
            "payment_method": request.POST.get("payment_method", "cash"),
        }
        try:
            requests.post(f"{ORDER_SERVICE_URL}/api/orders/", json=data)
        except requests.exceptions.ConnectionError:
            pass
    return render(request, "create_order.html", {"customer_id": customer_id})


def order_list(request):
    orders = []
    customer_id = request.GET.get("customer_id")
    try:
        url = f"{ORDER_SERVICE_URL}/api/orders/list/"
        if customer_id:
            url += f"?customer_id={customer_id}"
        r = requests.get(url)
        if r.status_code == 200:
            orders = r.json()
    except requests.exceptions.ConnectionError:
        pass
    return render(request, "orders.html", {"orders": orders})


# ===== Reviews =====
def book_reviews(request, book_id):
    reviews_data = {}
    try:
        r = requests.get(f"{COMMENT_RATE_SERVICE_URL}/api/reviews/book/{book_id}/")
        if r.status_code == 200:
            reviews_data = r.json()
    except requests.exceptions.ConnectionError:
        pass
    return render(request, "reviews.html", {"reviews_data": reviews_data, "book_id": book_id})


def add_review(request, book_id):
    if request.method == "POST":
        data = {
            "book_id": book_id,
            "customer_id": int(request.POST.get("customer_id")),
            "rating": int(request.POST.get("rating")),
            "comment": request.POST.get("comment", ""),
        }
        try:
            requests.post(f"{COMMENT_RATE_SERVICE_URL}/api/reviews/", json=data)
        except requests.exceptions.ConnectionError:
            pass
    return render(request, "add_review.html", {"book_id": book_id})


# ===== Recommendations =====
def recommendations(request):
    recs = {}
    try:
        r = requests.get(f"{RECOMMENDER_SERVICE_URL}/api/recommendations/")
        if r.status_code == 200:
            recs = r.json()
    except requests.exceptions.ConnectionError:
        pass
    return render(request, "recommendations.html", {"recs": recs})
