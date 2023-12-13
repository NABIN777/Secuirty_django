from django import forms
from django.forms import ModelForm

from .models import Category, Clothes, Order


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = "__all__"


class ClotheForm(ModelForm):
    class Meta:
        model = Clothes
        fields = "__all__"

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['quantity', 'contact_no', 'contact_address']