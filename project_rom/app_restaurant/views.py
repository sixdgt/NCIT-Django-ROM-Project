from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from app_restaurant.forms import MenuCreateForm
from app_restaurant.models import Menu, Category
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.
def landing_page(request):
    return render(request, "landing.html")
# @login_required(login_url='login')
# def menu_list(request):
#     if request.method == "GET" and "search" in request.GET:
#         search_query = request.GET.get("search")
#         #search_query = request.GET['search']
#         # filter based on menu_title or menu_category
#         data = Menu.objects.filter(Q(menu_title__icontains=search_query) | Q(
#                         menu_category__category_name__icontains=search_query))
#         # filter based on both menu_title and menu_category
#         # data = Menu.objects.filter(menu_title__icontains=search_query, 
#         #                menu_category__category_name__icontains=search_query)
#         context = {
#             "menus": data
#         }
#     else:
#         context = {
#             "menus": Menu.objects.all()
#         }
#     return render(request, "menu_list.html", context)

@login_required(login_url='login')
def menu_list(request):
    # Search logic
    if request.method == "GET" and "search" in request.GET:
        search_query = request.GET.get("search")
        # Filter based on menu_title OR menu_category name
        menu_queryset = Menu.objects.filter(
            Q(menu_title__icontains=search_query) | 
            Q(menu_category__category_name__icontains=search_query)
        ).order_by('-id')
    else:
        menu_queryset = Menu.objects.all().order_by('-id')

    # Pagination Logic
    # We use 5 per page to match your Product List settings
    paginator = Paginator(menu_queryset, 5) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "menus": page_obj, # This now contains the paginated object
    }
    return render(request, "menu_list.html", context)

@login_required(login_url="login")
def menu_create(request):
    # Pass POST data or None to handle both initial load and submission
    form = MenuCreateForm(request.POST or None)
    
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "New dish added to the menu successfully!")
            return redirect("menu.list")
        else:
            messages.error(request, "Failed to add menu item. Please check the form.")
    
    context = {
        "title": "Add New Dish",
        "form": form,
        "button_text": "Create Dish"
    }
    return render(request, "menu_form.html", context)

@login_required(login_url="login")
def menu_edit(request, pk):
    # Use get_object_or_404 for better error handling (404 instead of 500)
    menu_item = get_object_or_404(Menu, id=pk)
    
    # Instance is passed to pre-fill the form
    form = MenuCreateForm(request.POST or None, instance=menu_item)
    
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, f"'{menu_item.menu_title}' updated successfully!")
            return redirect("menu.list")
        else:
            messages.error(request, "Update failed. Please correct the errors.")

    context = {
        "title": f"Edit Dish: {menu_item.menu_title}",
        "form": form,
        "button_text": "Update Dish"
    }
    return render(request, "menu_form.html", context) # Note: Using the same template!

@login_required(login_url='login')
def menu_detail(request, pk):
    menu_data = Menu.objects.get(id=pk)
    context = {
        'data': menu_data
    }
    return render(request, "menu_detail.html", context)

@login_required(login_url='login')
def menu_delete(request, pk):
    # Use get_object_or_404 to handle missing IDs gracefully
    menu_item = get_object_or_404(Menu, id=pk)
    
    if request.method == "POST":
        menu_item.delete()
        messages.warning(request, f"'{menu_item.menu_title}' has been removed from the menu.")
        return redirect("menu.list")
    
    # If GET, show the confirmation page
    return render(request, "menu_delete.html", {"menu": menu_item})