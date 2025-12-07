from django.shortcuts import render
from django.http import HttpResponse
from app_restaurant.forms import MenuCreateForm
# Create your views here.
def demo(request):
    return HttpResponse("Hello, this is a demo view!")

def menus(request):
    menu_form = MenuCreateForm()
    context = {
        "menu_title": "Pasta",
        "menu_price": "Rs. 300.00",
        "form": menu_form
    }
    #context.setdefault("form", menu_form)
    return render(request, "menus.html", context)