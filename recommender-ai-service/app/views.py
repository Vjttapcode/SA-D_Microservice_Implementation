from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests

COMMENT_RATE_SERVICE_URL = "http://comment-rate-service:8000"
BOOK_SERVICE_URL = "http://book-service:8000"


class RecommendBooks(APIView):
    def get(self, request):
        """
        Recommend books based on top-rated books from comment-rate-service.
        """
        recommendations = []
        try:
            # Get top-rated books from comment-rate-service
            r = requests.get(f"{COMMENT_RATE_SERVICE_URL}/api/reviews/top-rated/")
            if r.status_code == 200:
                top_rated = r.json()
                for item in top_rated:
                    book_id = item.get("book_id")
                    avg_rating = item.get("avg_rating")
                    # Get book details from book-service
                    try:
                        br = requests.get(f"{BOOK_SERVICE_URL}/api/books/{book_id}/")
                        if br.status_code == 200:
                            book = br.json()
                            book["avg_rating"] = avg_rating
                            recommendations.append(book)
                    except requests.exceptions.ConnectionError:
                        recommendations.append({
                            "book_id": book_id,
                            "avg_rating": avg_rating
                        })
        except requests.exceptions.ConnectionError:
            pass

        if not recommendations:
            # Fallback: return all books if no ratings yet
            try:
                r = requests.get(f"{BOOK_SERVICE_URL}/api/books/")
                if r.status_code == 200:
                    recommendations = r.json()[:10]
            except requests.exceptions.ConnectionError:
                pass

        return Response({
            "recommendations": recommendations,
            "strategy": "top-rated" if recommendations else "none"
        })


class RecommendForCustomer(APIView):
    def get(self, request, customer_id):
        """
        Recommend books for a specific customer based on their ratings
        and popular books they haven't rated yet.
        """
        recommendations = []
        try:
            # Get all reviews
            r = requests.get(f"{COMMENT_RATE_SERVICE_URL}/api/reviews/")
            if r.status_code == 200:
                all_reviews = r.json()
                # Find books the customer already rated
                customer_book_ids = {
                    rev["book_id"] for rev in all_reviews
                    if rev["customer_id"] == customer_id
                }
                # Get top-rated books
                tr = requests.get(f"{COMMENT_RATE_SERVICE_URL}/api/reviews/top-rated/")
                if tr.status_code == 200:
                    for item in tr.json():
                        if item["book_id"] not in customer_book_ids:
                            try:
                                br = requests.get(f"{BOOK_SERVICE_URL}/api/books/{item['book_id']}/")
                                if br.status_code == 200:
                                    book = br.json()
                                    book["avg_rating"] = item["avg_rating"]
                                    recommendations.append(book)
                            except requests.exceptions.ConnectionError:
                                pass
        except requests.exceptions.ConnectionError:
            pass

        return Response({
            "customer_id": customer_id,
            "recommendations": recommendations[:5]
        })
