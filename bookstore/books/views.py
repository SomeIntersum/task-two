from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from books.form import RentalForm
from books.models import Book, Category, Rental, Purchase


# Create your views here.
def home(request):
    books = Book.objects.all()

    now = timezone.now()
    upcoming_end_date = now + timedelta(days=7)

    upcoming_rentals = Rental.objects.filter(rental_end_date__gte=now, rental_end_date__lte=upcoming_end_date)

    upcoming_notifications = []
    for rental in upcoming_rentals:
        if rental.user == request.user:
            upcoming_notifications.append(
                f"Срок аренды книги '{rental.book.title}' заканчивается {rental.rental_end_date.strftime('%Y-%m-%d')}.")

    return render(request, 'books/home.html', {'books': books, 'upcoming_notifications': upcoming_notifications})


def book_list(request):
    categories = Category.objects.all()
    authors = Book.objects.values_list('author', flat=True).distinct()
    years = Book.objects.values_list('publication_year', flat=True).distinct()

    selected_category = request.GET.get('category')
    selected_author = request.GET.get('author')
    selected_year = request.GET.get('year')

    books = Book.objects.all()

    if selected_category:
        books = books.filter(category__slug=selected_category)
    if selected_author:
        books = books.filter(author=selected_author)
    if selected_year:
        books = books.filter(publication_year=selected_year)

    context = {
        'books': books,
        'categories': categories,
        'authors': authors,
        'years': years,
        'selected_category': selected_category,
        'selected_author': selected_author,
        'selected_year': selected_year,
    }

    return render(request, 'books/book_list.html', context)


@login_required
def book_detail(request, slug):
    book = get_object_or_404(Book, slug=slug)

    is_purchased = Purchase.objects.filter(user=request.user, book=book).exists()

    is_rented = Rental.objects.filter(user=request.user, book=book).exists()

    return render(request, 'books/book_detail.html', {
        'book': book,
        'is_purchased': is_purchased,
        'is_rented': is_rented,
    })

@login_required
def rent_book(request, book_slug):
    book = get_object_or_404(Book, slug=book_slug)

    if request.method == 'POST':
        form = RentalForm(request.POST)
        if form.is_valid():
            rental_period = form.cleaned_data['rental_period']

            if rental_period == '2W':
                rental_end_date = timezone.now() + timezone.timedelta(weeks=2)
            elif rental_period == '1M':
                rental_end_date = timezone.now() + timezone.timedelta(days=30)
            elif rental_period == '3M':
                rental_end_date = timezone.now() + timezone.timedelta(days=90)

            rental = Rental.objects.create(
                book=book,
                user=request.user,
                rental_start_date=timezone.now(),
                rental_end_date=rental_end_date,
                rental_period=rental_period
            )
            return redirect('rental_success', rental_id=rental.id)
    else:
        form = RentalForm()

    return render(request, 'books/rent_book.html', {'book': book, 'form': form})


@login_required
def buy_book(request, book_slug):
    book = get_object_or_404(Book, slug=book_slug)

    if request.method == 'POST':
        Purchase.objects.create(
            book=book,
            user=request.user,
        )
        return redirect('buy_success', book_slug=book.slug)

    return render(request, 'books/buy_book.html', {'book': book})


@login_required
def rental_success(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id)
    return render(request, 'books/rental_success.html', {'rental': rental})


@login_required
def buy_success(request, book_slug):
    book = get_object_or_404(Book, slug=book_slug)
    return render(request, 'books/buy_success.html', {'book': book})


@login_required
def purchases_and_rentals(request):
    purchased_books = Purchase.objects.filter(user=request.user)

    rented_books = Rental.objects.filter(user=request.user)

    return render(request, 'books/purchases_and_rentals.html', {
        'purchased_books': purchased_books,
        'rented_books': rented_books,
    })
