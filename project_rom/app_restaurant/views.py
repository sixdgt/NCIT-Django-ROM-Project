from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def demo(request):
    return HttpResponse("Hello, this is a demo view!")

def menus(request):
    context = {
        "menu_title": "Pasta",
        "menu_price": "Rs. 300.00"
    }
    return render(request, "menus.html", context)