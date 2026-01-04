from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.
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
            return redirect('dashboad')
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
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        # checking password and confirm password
        if password != confirm_password:
            messages.add_message(request, messages.ERROR, "Password do not match!!")
            return redirect('register')
        # checking if email already exist (Note: same for username)
        if User.objects.filter(email=email):
            messages.add_message(request, messages.ERROR, "Email already registered!")
            return redirect('register')
        if User.objects.filter(username=username):
            messages.add_message(request, messages.ERROR, "Username already taken!")
            return redirect('register')
        # creating user
        user = User.objects.create_user(
            full_name=full_name,
            username=username,
            email=email,
            password=password
        )
        user.save()
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