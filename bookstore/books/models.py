from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название категории"
    )
    slug = models.SlugField(unique=True, verbose_name="Слаг")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Book(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Название книги"
    )
    slug = models.SlugField(unique=True, verbose_name="Слаг")
    author = models.CharField(
        max_length=200,
        verbose_name="Автор книги"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Категория"
    )
    publication_year = models.PositiveIntegerField(
        verbose_name="Год публикации"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена"
    )
    is_available = models.BooleanField(
        default=True,
        verbose_name="Доступна ли книга"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"


class Rental(models.Model):
    RENTAL_PERIOD_CHOICES = [
        ('2W', '2 недели'),
        ('1M', '1 месяц'),
        ('3M', '3 месяца'),
    ]

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        verbose_name="Книга"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    rental_start_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="Дата начала аренды"
    )
    rental_end_date = models.DateTimeField(
        verbose_name="Дата окончания аренды"
    )
    rental_period = models.CharField(
        max_length=2,
        choices=RENTAL_PERIOD_CHOICES,
        verbose_name="Срок аренды"
    )

    def __str__(self):
        return f"{self.user.username} арендовал {self.book.title}"

    def is_overdue(self):
        return timezone.now() > self.rental_end_date

    class Meta:
        verbose_name = "Аренда"
        verbose_name_plural = "Аренды"


class RentalNotification(models.Model):
    rental = models.OneToOneField(
        Rental,
        on_delete=models.CASCADE,
        verbose_name="Аренда"
    )
    notification_sent = models.BooleanField(
        default=False,
        verbose_name="Уведомление отправлено"
    )

    def __str__(self):
        return f"Уведомление для аренды {self.rental.id}"

    class Meta:
        verbose_name = "Уведомление об аренде"
        verbose_name_plural = "Уведомления об аренде"


class Purchase(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        verbose_name="Книга"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    purchase_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="Дата покупки"
    )

    def __str__(self):
        return f"{self.user.username} купил {self.book.title}"

    class Meta:
        verbose_name = "Покупка"
        verbose_name_plural = "Покупки"
