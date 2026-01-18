from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from app_restaurant.models import Menu, Category
from app_orders.models import Table, Order, OrderItem, Customer
from django.contrib import messages
from django.db.models import Sum, Count
from django.utils import timezone
from .utils import render_to_pdf
from django.http import HttpResponse
import uuid
from django.db.models import Q
from django.db import transaction

# Create your views here.
@login_required(login_url='login')
def quick_restock(request, menu_id):
    if request.method == "POST":
        menu_item = get_object_or_404(Menu, id=menu_id)
        amount = int(request.POST.get('amount', 0))
        
        menu_item.stock_quantity += amount
        if menu_item.stock_quantity > 0:
            menu_item.is_available = True # Re-enable if it was sold out
        menu_item.save()
        
        messages.success(request, f"Added {amount} units to {menu_item.menu_title}.")
    return redirect('low_stock_report')

@login_required(login_url='login')
def low_stock_report(request):
    # Items with 0 stock (Out of stock)
    out_of_stock = Menu.objects.filter(stock_quantity=0)
    
    # Items with low stock (e.g., between 1 and 10)
    low_stock_threshold = 10
    low_stock = Menu.objects.filter(stock_quantity__gt=0, stock_quantity__lte=low_stock_threshold)
    
    context = {
        'out_of_stock': out_of_stock,
        'low_stock': low_stock,
        'threshold': low_stock_threshold
    }
    return render(request, 'low_stock.html', context)

@login_required(login_url='login')
def process_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == "POST":
        # 1. Capture payment details from form
        discount = float(request.POST.get('discount', 0.0))
        payment_method = request.POST.get('payment_method', 'Cash')
        
        # 2. Update Order Financials
        # Total Price is already set, but we apply VAT/Discount logic
        # Example: 13% VAT
        vat_rate = 0.13 
        order.discounted_price = discount
        order.vat_amount = (order.total_price - discount) * vat_rate
        order.payment_method = payment_method
        order.payment_status = True
        order.order_status = 'COMPLETED'
        order.save()
        
        # 3. Release the Table
        table = order.table
        table.table_status = True  # Set back to Available
        table.save()
        
        messages.success(request, f"Payment processed for {order.order_code}. Table {table.table_number} is now free.")
        return redirect('sales_report')

    return render(request, 'process_payment.html', {'order': order})

@login_required(login_url='login')
def table_list(request):
    tables = Table.objects.all().order_by('table_number')
    
    if request.method == "POST":
        number = request.POST.get('table_number')
        capacity = request.POST.get('table_capacity')
        
        # Check if table number already exists
        if Table.objects.filter(table_number=number).exists():
            messages.error(request, f"Table {number} already exists!")
        else:
            Table.objects.create(table_number=number, table_capacity=capacity)
            messages.success(request, f"Table {number} added to floor plan.")
        return redirect('table_list')
        
    return render(request, 'table_list.html', {'tables': tables})

@login_required(login_url='login')
def table_update(request, pk):
    table = get_object_or_404(Table, pk=pk)
    
    if request.method == "POST":
        table.table_number = request.POST.get('table_number')
        table.table_capacity = request.POST.get('table_capacity')
        # Allow manager to manually reset status if needed
        table.table_status = 'table_status' in request.POST 
        table.save()
        messages.success(request, f"Table {table.table_number} updated.")
        return redirect('table_list')
        
    return render(request, 'tables/table_form.html', {'table': table})

@login_required(login_url='login')
def table_delete(request, pk):
    table = get_object_or_404(Table, pk=pk)
    
    # Prevent deletion if table is currently occupied (False)
    if not table.table_status:
        messages.error(request, "Cannot delete an occupied table. Please clear the order first.")
    else:
        table.delete()
        messages.success(request, "Table removed from floor plan.")
        
    return redirect('table_list')

@login_required(login_url='login')
def generate_receipt_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    items = OrderItem.objects.filter(order=order)
    
    data = {
        'order': order,
        'items': items,
        'today': timezone.now(),
    }
    
    pdf = render_to_pdf('receipt_pdf.html', data)
    
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"Receipt_Order_{order_id}.pdf"
        content = f"inline; filename={filename}"
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Error generating PDF", status=400)

@login_required(login_url='login')
def sales_report(request):
    # Get today's date
    today = timezone.now().date()
    
    # 1. Basic Stats for today
    # Mapping: created_at -> order_date | status -> order_status
    todays_orders = Order.objects.filter(
        order_date__date=today, 
        order_status='COMPLETED' # Use the uppercase value if that's your model choice
    )

    # 2. Most Popular Items (Top 5)
    # Mapping: menu_item -> menu
    popular_items = OrderItem.objects.filter(order__in=todays_orders) \
        .values('menu__menu_title') \
        .annotate(total_qty=Sum('quantity')) \
        .order_by('-total_qty')[:5]

    total_revenue = todays_orders.aggregate(Sum('total_price'))['total_price__sum'] or 0
    total_count = todays_orders.count()

    # Calculate Average Order Value
    if total_count > 0:
        avg_order_value = total_revenue / total_count
    else:
        avg_order_value = 0

    context = {
        'total_revenue': total_revenue,
        'total_count': total_count,
        'avg_order_value': avg_order_value, # Pass it here
        'popular_items': popular_items,
        'recent_orders': todays_orders.order_by('-order_date')[:10]
    }
    return render(request, 'sales_report.html', context)

@login_required(login_url='login')
def kitchen_dashboard(request):
    active_tickets = Order.objects.filter(
        order_status__in=['PENDING', 'IN_PROGRESS']
    ).order_by('order_date')
    
    return render(request, 'kitchen_dashboard.html', {'tickets': active_tickets})

@login_required(login_url='login')
def update_kitchen_status(request, order_id, new_status):
    order = get_object_or_404(Order, id=order_id)
    # Valid choices based on your model: 'PENDING', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED'
    order.order_status = new_status
    order.save()
    
    messages.success(request, f"Ticket #{order.order_code} updated to {new_status}.")
    return redirect('kitchen_dashboard')

@login_required(login_url='login')
def cancel_kitchen_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.order_status = 'CANCELLED'
    # Important: Free the table if the order is cancelled
    if order.table:
        order.table.table_status = True # Set to Available
        order.table.save()
    order.save()
    
    messages.warning(request, f"Ticket #{order.order_code} has been cancelled.")
    return redirect('kitchen_dashboard')

@login_required(login_url='login')
def update_order_status(request, order_id, new_status):
    # Retrieve order using correct field names
    order = get_object_or_404(Order, id=order_id)
    
    # Update 'order_status' (not 'status')
    order.order_status = new_status
    order.save()
    
    # Operational Logic: If order is completed, we might want to trigger other events
    if new_status == 'COMPLETED':
        messages.success(request, f"Order {order.order_code} is ready for serving!")
    
    return redirect('kitchen_dashboard')

@login_required(login_url='login')
def order_history(request):
    query = request.GET.get('q')
    if query:
        # Update the filter to use 'order_status' instead of 'status'
        orders = Order.objects.filter(
            Q(order_code__icontains=query) | 
            Q(customer__customer_name__icontains=query) |
            Q(order_status__icontains=query) # Fixed here
        ).order_by('-order_date')
    else:
        orders = Order.objects.all().order_by('-order_date')[:50]
        
    return render(request, 'order_history.html', {'orders': orders, 'query': query})

@login_required(login_url='login')
@transaction.atomic
def submit_final_order(request):
    if request.method == "POST":
        cart = request.session.get('order_cart', {})
        if not cart:
            messages.error(request, "Cart is empty!")
            return redirect('order_management')

        table_id = request.POST.get('table_id')
        customer_id = request.POST.get('customer_id')
        
        table = get_object_or_404(Table, id=table_id)
        customer = Customer.objects.filter(id=customer_id).first() if customer_id else None

        # 1. Create the Order
        order_code = f"ORD-{uuid.uuid4().hex[:6].upper()}"
        new_order = Order.objects.create(
            order_code=order_code,
            customer=customer,
            table=table,
            order_status='PENDING',
            total_price=0,
        )

        running_total = 0
        
        # 2. Iterate through cart items with Stock Logic
        for menu_id, qty in cart.items():
            menu_item = Menu.objects.get(id=menu_id)
            quantity = int(qty)

            # --- LOW STOCK LOGIC START ---
            if menu_item.stock_quantity < quantity:
                messages.error(request, f"Sorry, only {menu_item.stock_quantity} units of {menu_item.menu_title} left.")
                # Rollback happens automatically due to @transaction.atomic
                return redirect('order_management')

            # Deduct stock
            menu_item.stock_quantity -= quantity
            
            # If out of stock, set availability to False
            if menu_item.stock_quantity == 0:
                # Assuming you have an is_available field
                menu_item.table_status = False # Or menu_item.is_available = False
            
            menu_item.save()
            # --- LOW STOCK LOGIC END ---

            price_for_qty = menu_item.menu_price * quantity
            running_total += price_for_qty
            
            OrderItem.objects.create(
                order=new_order,
                menu=menu_item,
                quantity=quantity,
                item_price=menu_item.menu_price
            )

        # 3. Finalize Order and Table
        new_order.total_price = running_total
        new_order.save()
        
        table.table_status = False # Set table to 'Occupied'
        table.save()

        request.session['order_cart'] = {}
        messages.success(request, f"Order {order_code} placed successfully!")
        return redirect('order_management')

@login_required(login_url='login')
def order_management(request):
    # Fetch data for the left-side menu
    categories = Category.objects.all()
    query = request.GET.get('search')
    category_filter = request.GET.get('category')

    menus = Menu.objects.all()
    if query:
        menus = menus.filter(menu_title__icontains=query)
    if category_filter and category_filter != 'all':
        menus = menus.filter(menu_category__category_name=category_filter)

    # Process the Session Cart
    cart = request.session.get('order_cart', {})
    order_items = []
    order_total = 0

    for menu_id, quantity in cart.items():
        menu_item = get_object_or_404(Menu, id=menu_id)
        subtotal = menu_item.menu_price * quantity
        order_total += subtotal
        order_items.append({
            'menu': menu_item,
            'quantity': quantity,
            'subtotal': subtotal
        })

    context = {
        'menus': menus,
        'categories': categories,
        'tables': Table.objects.all(),
        'customers': Customer.objects.all(),
        'order_items': order_items,
        'order_total': order_total,
    }
    return render(request, 'order_management.html', context)

@login_required(login_url='login')
def add_to_order(request, menu_id):
    cart = request.session.get('order_cart', {})
    cart[str(menu_id)] = cart.get(str(menu_id), 0) + 1
    request.session['order_cart'] = cart
    return redirect('order_management')

@login_required(login_url='login')
def reduce_order_item(request, menu_id):
    cart = request.session.get('order_cart', {})
    if str(menu_id) in cart:
        cart[str(menu_id)] -= 1
        if cart[str(menu_id)] <= 0:
            del cart[str(menu_id)]
    request.session['order_cart'] = cart
    return redirect('order_management')

@login_required(login_url='login')
def remove_from_order(request, menu_id):
    cart = request.session.get('order_cart', {})
    if str(menu_id) in cart:
        del cart[str(menu_id)]
    request.session['order_cart'] = cart
    return redirect('order_management')

@login_required(login_url='login')
def clear_order(request):
    if 'order_cart' in request.session:
        del request.session['order_cart']
    return redirect('order_management')
