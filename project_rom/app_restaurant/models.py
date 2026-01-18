from django.db import models
from django.utils import timezone
# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=100, 
                                     null=False, blank=False)
    category_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.category_name

class Menu(models.Model):
    menu_title = models.CharField(max_length=200, null=False, blank=False)
    menu_price = models.FloatField(null=False, blank=False)
    menu_category = models.ForeignKey(Category, 
                                      max_length=100,
                                        null=False, 
                                        blank=False, 
                                        on_delete=models.CASCADE)
    menu_description = models.TextField(null=True, blank=True)
    menu_image = models.ImageField(upload_to='menu_images/', 
                                   null=True, blank=True)
    menu_status = models.BooleanField(default=True)
    stock_quantity = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.menu_title

