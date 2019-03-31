from django import forms
from .models import Order


class OrderCreateForm(forms.Form):
        address = forms.CharField(
            max_length=3000,
            widget=forms.Textarea())

