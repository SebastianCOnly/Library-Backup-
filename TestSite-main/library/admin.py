# Official_LMS/library/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Book, EBook

admin.site.register(CustomUser, UserAdmin)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publisher', 'quantity')
    search_fields = ('title', 'author', 'publisher')

@admin.register(EBook)
class EBookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publisher', 'quantity')
    search_fields = ('title', 'author', 'publisher')
