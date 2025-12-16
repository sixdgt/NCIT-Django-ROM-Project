from django.shortcuts import redirect, render
from django.http import HttpResponse
from app_restaurant.forms import MenuCreateForm
from app_restaurant.models import Menu, Category
# Create your views here.
def menu_list(request):
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
            return redirect("menu.list")
        else:
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
            return redirect("menu.list")
        else:
            return redirect("menu.edit", pk=pk)
    else:
        context = { "form": form }
        return render(request, "menu_edit.html", context)