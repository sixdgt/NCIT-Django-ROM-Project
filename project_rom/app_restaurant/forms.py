from app_restaurant.models import Menu
from django import forms

class MenuCreateForm(forms.ModelForm):

    class Meta:
        model = Menu
        fields = ['menu_title', 'menu_price', 'menu_category', 'menu_description']
        widgets = {
            'menu_title': forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Enter menu title'}),
            'menu_price': forms.NumberInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Enter menu price'}),
            'menu_category': forms.Select(attrs={'class': 'form-control mb-3'}),
            'menu_description': forms.Textarea(attrs={'class': 'form-control mb-3', 'placeholder': 'Enter menu description'}),
        }
        labels = {
            'menu_title': 'Menu Title',
            'menu_price': 'Menu Price',
            'menu_category': 'Menu Category',
            'menu_description': 'Menu Description',
        }