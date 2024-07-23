# Official_LMS/library/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, timedelta

def default_due_date():
    return datetime.now() + timedelta(days=14)

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=100, null=True, blank=True)  # Temporary nullable

    def __str__(self):
        return self.username

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, null=True, blank=True)  # Temporary nullable
    publisher = models.CharField(max_length=255, null=True, blank=True)  # Temporary nullable
    photo = models.ImageField(upload_to='book_photos/', null=True, blank=True)  # Temporary nullable
    quantity = models.PositiveIntegerField(null=True, blank=True)  # Temporary nullable

    def __str__(self):
        return self.title

class EBook(Book):
    pdf = models.FileField(upload_to='ebook_pdfs/')

class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.quantity})"

class Transaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    date_returned = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(default=default_due_date)

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.date})"
