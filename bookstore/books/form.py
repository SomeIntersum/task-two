from django import forms


class RentalForm(forms.Form):
    RENTAL_PERIOD_CHOICES = [
        ('2W', '2 недели'),
        ('1M', '1 месяц'),
        ('3M', '3 месяца'),
    ]

    rental_period = forms.ChoiceField(
        choices=RENTAL_PERIOD_CHOICES,
        label="Срок аренды",
        widget=forms.RadioSelect
    )
