# Official_LMS/library/urls.py

from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.books, name='books'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('my_bag/', views.my_bag, name='my_bag'),
    path('returns/', views.returns, name='returns'),
    path('readers/', views.readers, name='readers'),
    path('add_to_cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('account_details/', views.account_details, name='account_details'),
    path('edit_account_details/', views.edit_account_details, name='edit_account_details'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('return_book/<int:transaction_id>/', views.return_book, name='return_book'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('renew_book/<int:transaction_id>/', views.renew_book, name='renew_book'),
]
