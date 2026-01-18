from app_restaurant.models import Menu
from django import forms

class MenuCreateForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['menu_title', 'menu_category', 'menu_price', 'menu_description']
        
        widgets = {
            "menu_title": forms.TextInput(attrs={
                "class": "form-control form-control-lg mb-2", 
                "placeholder": "e.g. Grilled Mediterranean Salmon"
            }),
            "menu_category": forms.Select(attrs={
                "class": "form-select form-control-lg mb-2"
            }),
            "menu_price": forms.NumberInput(attrs={
                "class": "form-control form-control-lg mb-2", 
                "placeholder": "0.00"
            }),
            "menu_description": forms.Textarea(attrs={
                "class": "form-control mb-2", 
                "placeholder": "Describe the ingredients, allergens, or preparation style...",
                "rows": 4
            }),
        }
        
        labels = {
            "menu_title": "Dish Name",
            "menu_category": "Menu Category",
            "menu_price": "Price ($)",
            "menu_description": "Dish Description",
        }