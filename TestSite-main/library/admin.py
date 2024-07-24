# Official_LMS/library/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Book, EBook, Transaction
from django.utils.html import format_html
from datetime import timedelta

# Custom action to extend book rentals
def extend_rental(modeladmin, request, queryset):
    for transaction in queryset:
        if not transaction.renewed:
            transaction.due_date += timedelta(days=7)
            transaction.renewed = True
            transaction.save()
            modeladmin.message_user(request, f'Rental for {transaction.book.title} extended.')
        else:
            modeladmin.message_user(request, f'Rental for {transaction.book.title} has already been extended.')

extend_rental.short_description = "Extend rental by 7 days"

# Admin configuration for the Transaction model
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'date_checked_out', 'due_date', 'date_returned', 'renewed')
    actions = [extend_rental]

    def date_checked_out(self, obj):
        return obj.date
    date_checked_out.short_description = 'Date Checked Out'

# Custom user admin to display checked-out books and user type
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'full_name', 'is_staff', 'is_superuser', 'date_joined', 'last_login')
    readonly_fields = ('checked_out_books',)

    def checked_out_books(self, obj):
        transactions = Transaction.objects.filter(user=obj, date_returned__isnull=True)
        if transactions.exists():
            books = [f'{t.book.title} (Due: {t.due_date})' for t in transactions]
            return format_html('<br>'.join(books))
        return 'No books checked out'

    checked_out_books.short_description = 'Checked Out Books'

admin.site.register(CustomUser, CustomUserAdmin)

# Admin configuration for the Book model
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publisher', 'quantity')
    search_fields = ('title', 'author', 'publisher')

# Admin configuration for the EBook model
@admin.register(EBook)
class EBookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publisher', 'quantity')
    search_fields = ('title', 'author', 'publisher')