from django.urls import path
from api.views import (
    MenuListCreateAPIView
)
urlpatterns = [
    # Define your API endpoints here
    # will work for both GET /api/menus/ to get menu list
    # and POST to /api/menus/ to create new menu item
    path('menus/', MenuListCreateAPIView.as_view(), name='menu-list-create'),
]