# Official_LMS/library/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import CustomUserCreationForm, UserUpdateForm
from .models import Book, EBook, CartItem, Transaction, CustomUser
from datetime import datetime, timedelta
from .forms import CustomPasswordChangeForm

def home(request):
    return render(request, 'home.html')

def books(request):
    query = request.GET.get('q')
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query) | Q(publisher__icontains=query)
        )
        ebooks = EBook.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query) | Q(publisher__icontains=query)
        )
    else:
        books = Book.objects.all()
        ebooks = EBook.objects.all()
    return render(request, 'books.html', {'books': books, 'ebooks': ebooks, 'query': query})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'book_detail.html', {'book': book})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "Invalid username or password.")
        else:
            form.add_error(None, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def profile(request):
    user = request.user
    books = Book.objects.all()
    return render(request, 'account.html', {'user': user, 'books': books})

@login_required
def my_bag(request):
    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, 'my_bag.html', {'cart_items': cart_items})

@login_required
def returns(request):
    borrowed_books = Transaction.objects.filter(user=request.user, date_returned__isnull=True)
    return render(request, 'returns.html', {'borrowed_books': borrowed_books})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def account_view(request):
    return render(request, 'account.html')

@login_required
def readers(request):
    return render(request, 'readers.html')

@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if book.quantity > 0:
        cart_item, created = CartItem.objects.get_or_create(user=request.user, book=book)
        if not created:
            cart_item.quantity += 1
        cart_item.save()

        # Update the book's quantity
        book.quantity -= 1
        book.save()
        
        messages.success(request, f'{book.title} has been successfully added to your bag.')
    else:
        messages.error(request, f'No more copies of {book.title} are available.')

    return redirect('books')

@login_required
def checkout(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)
    for item in cart_items:
        book = item.book
        if book.quantity >= item.quantity:
            book.quantity -= item.quantity
            book.save()
            # Create a transaction for each book checked out
            Transaction.objects.create(
                user=user,
                book=book,
                date=datetime.now(),
                due_date=datetime.now() + timedelta(days=14)  # Set due date 14 days from now
            )
            item.delete()
        else:
            messages.error(request, f'Not enough copies of {book.title} available.')
    messages.success(request, 'Checkout successful!')
    return redirect('my_bag')

@login_required
def return_book(request, transaction_id):
        transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)
        book = transaction.book
        book.quantity += 1
        book.save()
        transaction.date_returned = datetime.now()
        transaction.save()
        messages.success(request, f'You have successfully returned {book.title}.')
        return redirect('returns')

@login_required
def account_details(request):
    user = request.user
    borrowed_books = Transaction.objects.filter(user=user, date_returned__isnull=True)
    return render(request, 'account_details.html', {
        'user': user,
        'borrowed_books': borrowed_books,
        'current_tab': 'account_details'
    })

@login_required
def edit_account_details(request):
    user_form = None
    password_form = None

    if request.method == 'POST':
        if 'update_details' in request.POST:
            user_form = UserUpdateForm(request.POST, instance=request.user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Your account details have been updated!')
                return redirect('account_details')
        elif 'change_password' in request.POST:
            password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')
                return redirect('account_details')
            else:
                messages.error(request, 'Please correct the error below.')
        elif 'delete_account' in request.POST:
            request.user.delete()
            messages.success(request, 'Your account has been deleted.')
            return redirect('home')
    else:
        user_form = UserUpdateForm(instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user)

    return render(request, 'edit_account_details.html', {
        'user_form': user_form,
        'password_form': password_form
    })

def delete_account(request):
    user = request.user
    user.delete()
    messages.success(request, 'Your account has been deleted.')
    return redirect('home')


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    book = cart_item.book
    book.quantity += cart_item.quantity
    book.save()
    cart_item.delete()
    messages.success(request, 'Item removed from your cart.')
    return redirect('my_bag')

@login_required
def renew_book(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)
    if transaction.renewed:
        messages.error(request, f'{transaction.book.title} has already been renewed once.')
    else:
        transaction.due_date += timedelta(days=7)
        transaction.renewed = True
        transaction.save()
        messages.success(request, f'You have successfully renewed {transaction.book.title} for another week.')
    return redirect('account_details')