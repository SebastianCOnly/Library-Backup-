# Official_LMS/library/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, timedelta

def default_due_date():
    """
    Returns a default due date 14 days from the current of when the user requests a book
    """
    return datetime.now() + timedelta(days=14)

class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    This allows adding extra fields or methods to the user model.
    """
    full_name = models.CharField(max_length=100, null=True, blank=True)  # Optional field for the user's full name.

    def __str__(self):
        """
        String representation of the CustomUser model.
        Returns the username of the user, which is used for display in the Django admin and other contexts.
        """
        return self.username

class Book(models.Model):
    """
    Model representing a book in the library.
    """
    title = models.CharField(max_length=255)  # Title of the book.
    author = models.CharField(max_length=255, null=True, blank=True)  # Author of the book, optional field.
    publisher = models.CharField(max_length=255, null=True, blank=True)  # Publisher of the book, optional field.
    photo = models.ImageField(upload_to='book_photos/', null=True, blank=True)  # Photo of the book cover, optional.
    quantity = models.PositiveIntegerField(null=True, blank=True)  # Number of copies available, optional.
    description = models.TextField(blank=True, null=True)  # Description or summary of the book, optional.

    def __str__(self):
        """
        String representation of the Book model.
        Returns the title of the book.
        """
        return self.title

class CartItem(models.Model):
    """
    Model representing an item in a user's cart.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # The user who owns this cart item.
    book = models.ForeignKey(Book, on_delete=models.CASCADE)  # The book associated with this cart item.
    quantity = models.PositiveIntegerField(default=1)  # Number of copies of the book in the cart.

    def __str__(self):
        """
        String representation of the CartItem model.
        Returns a string in the format 'username - book title (quantity)'.
        """
        return f"{self.user.username} - {self.book.title} ({self.quantity})"

class Transaction(models.Model):
    """
    Model representing a transaction, which records the borrowing of a book.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    date_returned = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(default=default_due_date)
    renewed = models.BooleanField(default=False)  # Flag indicating whether the book has been renewed.

    def __str__(self):
        """
        String representation of the Transaction model.
        """
        return f"{self.user.username} - {self.book.title} ({self.date})"
