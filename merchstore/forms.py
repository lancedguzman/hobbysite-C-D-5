from django import forms
from .models import Product, Transaction


class ProductForm(forms.ModelForm):
    """Creates the Product Form."""
    class Meta:
        model = Product
        exclude = ["owner",]


class UpdateForm(forms.ModelForm):
    """Creates the Product Update Form."""
    class Meta:
        model = Product
        exclude = ["owner",]
        

class TransactionForm(forms.ModelForm):
    """Creates the Transaction Form."""
    class Meta:
        model = Transaction
        fields = ["amount",]
