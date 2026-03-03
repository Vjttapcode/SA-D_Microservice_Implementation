from django.db import models


class Review(models.Model):
    book_id = models.IntegerField()
    customer_id = models.IntegerField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('book_id', 'customer_id')

    def __str__(self):
        return f"Review by Customer {self.customer_id} for Book {self.book_id} - {self.rating}/5"
