from django.urls import path
from accounts.views import (
    login_view, logout_view, dashboard, register_view
)
urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
] 