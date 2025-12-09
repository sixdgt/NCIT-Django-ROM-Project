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
    created_at = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.menu_title

class Customer(models.Model):
    customer_name = models.CharField(max_length=200,
                                     null=False, blank=False)
    customer_contact = models.CharField(max_length=15,
                                        null=False, blank=False)
    customer_address = models.CharField(max_length=255,
                                        null=True, blank=True)
    customer_email = models.EmailField(unique=True,
                                       null=False, blank=False)
    created_at = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.customer_name

class Table(models.Model):
    table_number = models.IntegerField(unique=True,
                                       null=False, blank=False)
    table_capacity = models.IntegerField(null=False, blank=False)
    table_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return f"Table {self.table_number}"

class Order(models.Model):
    ORDER_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    order_code = models.CharField(max_length=100,unique=True,null=False, blank=False)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    table = models.ForeignKey(Table,on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    order_status = models.CharField(choices=ORDER_CHOICES,max_length=50, 
                                    null=False, blank=False)
    discounted_price = models.FloatField(default=0.0)
    coupen_code = models.CharField(max_length=50, null=True, blank=True)
    vat_amount = models.FloatField(default=0.0)
    total_price = models.FloatField(null=False, blank=False)
    payment_method = models.CharField(max_length=50, null=True, blank=True)
    payment_status = models.BooleanField(default=False)

    def __str__(self):
        return self.order_code

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False)
    item_price = models.FloatField(null=False, blank=False)

    def __str__(self):
        return f"{self.quantity} x {self.menu.menu_title} \
            for Order {self.order.order_code}"


