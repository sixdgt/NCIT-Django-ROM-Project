from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
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
    return render(request, 'dashboard.html')