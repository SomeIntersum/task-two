from django.urls import path

from books.views import home, book_list, book_detail, rent_book, buy_book, rental_success, buy_success, \
    purchases_and_rentals

urlpatterns = [
    path('', home, name='home'),
    path('books/', book_list, name='book_list'),
    path('books/<slug:slug>/', book_detail, name='book_detail'),

    path('books/<slug:book_slug>/rent/', rent_book, name='rent_book'),
    path('books/<slug:book_slug>/buy/', buy_book, name='buy_book'),
    path('rental_success/<int:rental_id>/', rental_success, name='rental_success'),
    path('buy_success/<slug:book_slug>/', buy_success, name='buy_success'),
    path('purchases_and_rentals/', purchases_and_rentals, name='purchases_and_rentals'),

]
