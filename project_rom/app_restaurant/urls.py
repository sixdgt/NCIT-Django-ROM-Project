from django.urls import path
from app_restaurant.views import menu_list, menu_create, menu_edit

urlpatterns = [
    path('menu/list/', menu_list, name='menu.list'),
    path('menu/create/', menu_create, name='menu.create'),
    path('menu/edit/<int:pk>/', menu_edit, name='menu.edit'),
]