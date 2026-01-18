from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Sum
from django.utils import timezone
from app_orders.models import Order, Table
from app_restaurant.models import Menu

# Create your views here.
def send_notification_email(request, to_email, subject, message):
    """
    Utility function to send email notification
    """
    try:
        sender = settings.EMAIL_HOST_USER
        send_mail(subject, message, sender, [to_email], fail_silently=False)
        # in product do not show the email sent message for registration unless 
        # it is a verification email
        messages.add_message(request, messages.SUCCESS, "Email sent successfully!")
    except Exception as e:
        messages.add_message(request, messages.ERROR, f"Error sending email: {str(e)}")

def login_view(request):
    """
    It will handle the user login with django authentication
    """
    if request.method == "POST":
        # taking inputs from form i.e. login form
        username = request.POST.get('username')
        password = request.POST.get('password')
        # authenticating user
        user = authenticate(request, username=username, password=password)
        if user:
            # login session
            login(request, user)
            messages.add_message(request, messages.SUCCESS, "Login success!")
            return redirect('dashboard')
        else:
            messages.add_message(request, messages.ERROR, "Login failed!!")
            return redirect('login')
    return render(request, "login.html")

def register_view(request):
    """
    It will handle user registration
    """
    # taking inputs from user
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        # checking password and confirm password
        if password != confirm_password:
            messages.add_message(request, messages.ERROR, "Password do not match!!")
            return redirect('register')
        # checking if email already exist (Note: same for username)
        if User.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR, "Email already registered!")
            return redirect('register')
        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR, "Username already taken!")
            return redirect('register')
        # creating user
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password
        )
        user.save()
        send_notification_email(request, 
                                email,
                                "Account Creation",
                                "Welcome to our restaurant management system!")
        messages.add_message(request, messages.SUCCESS, 
                             "Registered successfully! Please login")
        return redirect('login')
    return render(request, 'register.html')

def logout_view(request):
    """
    It will handle logout
    """
    logout(request)
    return redirect("login")

@login_required(login_url='login') # checking login
def dashboard(request):
    today = timezone.now().date()
    
    # 1. Stats for the Top Cards
    todays_orders = Order.objects.filter(order_date__date=today)
    total_revenue = todays_orders.filter(order_status='COMPLETED').aggregate(Sum('total_price'))['total_price__sum'] or 0
    orders_count = todays_orders.count()
    total_menu_items = Menu.objects.count()
    
    # 2. Occupancy Calculation
    total_tables = Table.objects.count()
    occupied_tables = Table.objects.filter(table_status=False).count()
    occupancy_percent = int((occupied_tables / total_tables) * 100) if total_tables > 0 else 0

    # 3. Live Kitchen Tickets (Pending or In Progress)
    live_tickets = Order.objects.filter(
        order_status__in=['PENDING', 'IN_PROGRESS']
    ).order_by('-order_date')[:5]

    low_stock_threshold = 5
    low_stock_items = Menu.objects.filter(stock_quantity__lte=low_stock_threshold)
    low_stock_count = low_stock_items.count()

    context = {
        'low_stock_count': low_stock_count,
        'low_stock_items': low_stock_items,
        'total_revenue': total_revenue,
        'orders_today': orders_count,
        'total_products': total_menu_items,
        'occupancy_percent': occupancy_percent,
        'recent_transactions': live_tickets,
    }
    return render(request, 'dashboard.html', context)