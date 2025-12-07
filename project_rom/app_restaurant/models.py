from django.db import models

# Create your models here.
class Menu(models.Model):
    CATEGORY_CHOICES = [
        ('VEG', 'Vegetarian'),
        ('NON_VEG', 'Non-Vegetarian'),
        ('BEVERAGE', 'Beverage'),
        ('DESSERT', 'Dessert'),
        ('SNACKS', 'Snacks')
    ]
    menu_title = models.CharField(max_length=200, null=False, blank=False)
    menu_price = models.FloatField(null=False, blank=False)
    menu_category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, null=False, blank=False)
    menu_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.menu_title