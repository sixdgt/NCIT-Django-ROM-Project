from django.urls import path
from . import views

urlpatterns = [
    # --- Order & POS Paths ---
    path('order/', views.order_management, name='order_management'),
    path('order/add/<int:menu_id>/', views.add_to_order, name='add_to_order'),
    path('order/reduce/<int:menu_id>/', views.reduce_order_item, name='reduce_order_item'),
    path('order/remove/<int:menu_id>/', views.remove_from_order, name='remove_from_order'),
    path('order/clear/', views.clear_order, name='clear_order'),
    path('order/submit/', views.submit_final_order, name='submit_final_order'),
    path('orders/history/', views.order_history, name='order_history'),

    # --- Table & Payment Management ---
    path('tables/', views.table_list, name='table_list'),
    path('tables/edit/<int:pk>/', views.table_update, name='table_update'),
    path('tables/delete/<int:pk>/', views.table_delete, name='table_delete'),
    path('order/payment/<int:order_id>/', views.process_payment, name='process_payment'),
    path('inventory/restock/<int:menu_id>/', views.quick_restock, name='quick_restock'),

    # --- Kitchen Dashboard Paths ---
    path('kitchen/', views.kitchen_dashboard, name='kitchen_dashboard'),
    path('kitchen/status/<int:order_id>/<str:new_status>/', views.update_order_status, name='update_status'),
    path('kitchen/update/<int:order_id>/<str:new_status>/', views.update_kitchen_status, name='update_status'),
    path('kitchen/cancel/<int:order_id>/', views.cancel_kitchen_order, name='cancel_kitchen_order'),

    # --- Analytics & Reporting Paths ---
    path('reports/sales/', views.sales_report, name='sales_report'),
    path('reports/low-stock/', views.low_stock_report, name='low_stock_report'),

    # --- PDF Receipt Path ---
    path('order/receipt/<int:order_id>/', views.generate_receipt_pdf, name='generate_receipt'),
]