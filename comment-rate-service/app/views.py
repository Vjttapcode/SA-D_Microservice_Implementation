from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Review
from .serializers import ReviewSerializer
from django.db.models import Avg
import requests

BOOK_SERVICE_URL = "http://book-service:8000"


class ReviewListCreate(APIView):
    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request):
        book_id = request.data.get("book_id")
        # Validate book exists
        try:
            r = requests.get(f"{BOOK_SERVICE_URL}/api/books/{book_id}/")
            if r.status_code != 200:
                return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
        except requests.exceptions.ConnectionError:
            pass

        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookReviews(APIView):
    def get(self, request, book_id):
        reviews = Review.objects.filter(book_id=book_id)
        avg_rating = reviews.aggregate(avg=Avg('rating'))['avg']
        serializer = ReviewSerializer(reviews, many=True)
        return Response({
            "book_id": book_id,
            "average_rating": avg_rating,
            "reviews": serializer.data
        })


class TopRatedBooks(APIView):
    def get(self, request):
        top_books = (
            Review.objects.values('book_id')
            .annotate(avg_rating=Avg('rating'))
            .order_by('-avg_rating')[:10]
        )
        return Response(list(top_books))
