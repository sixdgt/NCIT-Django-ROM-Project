from rest_framework import serializers
from app_restaurant.models import Menu, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name', 'category_status', 'created_at']

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'menu_title', 'menu_description','menu_price',\
                   'menu_category','menu_status', 'created_at']
