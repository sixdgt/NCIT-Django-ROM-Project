from django.shortcuts import redirect, render
from django.http import HttpResponse
from app_restaurant.forms import MenuCreateForm
from app_restaurant.models import Menu, Category
from django.db.models import Q
from django.contrib import messages

# Create your views here.
def menu_list(request):
    if request.method == "GET" and "search" in request.GET:
        search_query = request.GET.get("search")
        #search_query = request.GET['search']
        # filter based on menu_title or menu_category
        data = Menu.objects.filter(Q(menu_title__icontains=search_query) | Q(
                        menu_category__category_name__icontains=search_query))
        # filter based on both menu_title and menu_category
        # data = Menu.objects.filter(menu_title__icontains=search_query, 
        #                menu_category__category_name__icontains=search_query)
        context = {
            "menus": data
        }
    else:
        context = {
            "menus": Menu.objects.all()
        }
    return render(request, "menu_list.html", context)

def menu_create(request):
    # check if the request method is POST
    if request.method == "POST":
        request_data = request.POST
        db_data = MenuCreateForm(request_data)
        if db_data.is_valid():
            db_data.save()
            messages.add_message(request, messages.SUCCESS, "Menu added successfully!!")
            return redirect("menu.list")
        else:
            messages.add_message(request, messages.ERROR, "Something went wrong!!")
            return redirect("menu.create")
    else:
        # if the request method is GET or page request then loading the form
        context = { "form": MenuCreateForm() }
        return render(request, "menu_create.html", context)

def menu_edit(request, pk):
    menu = Menu.objects.get(id=pk)
    form = MenuCreateForm(instance=menu)
    if request.method == "POST":
        request_data = request.POST
        db_data = MenuCreateForm(request_data, instance=menu)
        if db_data.is_valid():
            db_data.save()
            messages.add_message(request, messages.SUCCESS, "Menu udpated successfully!")
            return redirect("menu.list")
        else:
            messages.add_message(request, messages.ERROR, "Something went wrong!")
            return redirect("menu.edit", pk=pk)
    else:
        context = { "form": form }
        return render(request, "menu_edit.html", context)

def menu_detail(request, pk):
    menu_data = Menu.objects.get(id=pk)
    context = {
        'data': menu_data
    }
    return render(request, "menu_detail.html", context)

def menu_delete(request, pk):
    try:
        menu_data = Menu.objects.get(id=pk)
        menu_data.delete()
        messages.add_message(request, messages.ERROR, "Menu deleted successfully!")
        return redirect("menu.list")
    except Menu.DoesNotExist:
        messages.add_message(request, messages.WARNING, "Menu not found")
        return redirect("menu.list")