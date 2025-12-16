from django.contrib import admin
from app_restaurant.models import Category, Menu, Customer, Table,\
Order, OrderItem

# Register your models here.
class AdminMenu(admin.ModelAdmin):
    list_display = ["menu_title", "menu_category", "menu_price"] # columns to display
    search_fields = ["menu_title", "created_at"] # search data by fields
    list_filter = ["menu_category", "menu_status"] # filter data by fields

class AdminCategory(admin.ModelAdmin):
    list_display = ["category_name", "category_status"] 
    search_fields = ["category_name", "created_at"] 
    list_filter = ["category_status"]

admin.site.register(Category, AdminCategory) # FOR CATEGORY
admin.site.register(Menu, AdminMenu) # FOR MENU
admin.site.register(Customer)
admin.site.register(Table)
admin.site.register(Order)
admin.site.register(OrderItem)

# admin panel settings customization
admin.site.site_header = "Restaurant Order System"
admin.site.site_title = "Restaurant Order System | Admin Portal"
admin.site.index_title = "Best ROM in Nepal"
admin.site.empty_value_display = "-empty-"