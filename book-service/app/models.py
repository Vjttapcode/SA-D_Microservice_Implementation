from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    isbn = models.CharField(max_length=13, blank=True)
    category_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title
