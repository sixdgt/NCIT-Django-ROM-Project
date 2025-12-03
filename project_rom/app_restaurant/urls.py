from django.urls import path
from app_restaurant.views import demo, menus

urlpatterns = [
    path('demo/', demo, name='demo'),
    path('menus/', menus, name='menus'),
]