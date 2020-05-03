from django import forms


class SizeForm(forms.Form):
    CHOICES = (
        ('S', 'SMALL'),
        ('M', 'MEDIUM'),
        ('L', 'LARGE'),
    )
    size = forms.ChoiceField(
        choices=CHOICES, label='Select size',
        widget=forms.RadioSelect()
    )
    quantity = forms.IntegerField(min_value=1, max_value=5)
