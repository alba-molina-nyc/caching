from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['setter_fname', 'setter_lname', 'setter_email', 'note']