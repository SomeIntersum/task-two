from django.contrib import admin

from books.models import Category, Book, Rental, RentalNotification


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

    prepopulated_fields = {'slug': ('name',)}


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'publication_year', 'price', 'is_available')
    list_filter = ('category', 'author', 'publication_year', 'is_available')
    search_fields = ('title', 'author', 'category__name')
    ordering = ('-publication_year',)

    prepopulated_fields = {'slug': ('title',)}


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rental_start_date', 'rental_end_date', 'rental_period', 'is_overdue')
    list_filter = ('book', 'user', 'rental_period')
    search_fields = ('book__title', 'user__username')


@admin.register(RentalNotification)
class RentalNotificationAdmin(admin.ModelAdmin):
    list_display = ('rental', 'notification_sent')
    list_filter = ('notification_sent',)
    search_fields = ('rental__book__title', 'rental__user__username')
