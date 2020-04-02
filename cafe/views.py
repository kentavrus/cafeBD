from django.http import Http404
from django.shortcuts import render, redirect

from .models import Barist, Dish, Product, Invoice, User


# Create your views here.


def baristas(request):
    baristas_list = Barist.objects.all()
    return render(request, 'cafe/baristas.html', {"baristas": baristas_list})


def barista_detail(request, barista_ipn):
    try:
        barist = Barist.objects.get(ipn=barista_ipn)
    except:
        raise Http404("Barist not found")
    return render(request, 'cafe/barista.html', {"barista": barist})


def index(request):
    return render(request, 'index.html')


def dishes(request):
    try:
        dishes = Dish.objects.all()
    except:
        raise Http404("Dishes not found")
    return render(request, 'cafe/dishes.html', {"dishes": dishes})


def dish_detail(request, dish_id):
    try:
        dish = Dish.objects.get(id=dish_id)
    except:
        raise Http404("Dish not found")
    return render(request, 'cafe/dish.html', {"dish": dish})


def food(request):
    try:
        foods = Dish.objects.filter(type_of_dish="food")
    except:
        raise Http404("Foods not found")
    return render(request, 'cafe/food.html', {"foods": foods})


def drinks(request):
    try:
        drinks = Dish.objects.filter(type_of_dish="drink")
    except:
        raise Http404("Drinks not found")
    return render(request, 'cafe/drink.html', {"drinks": drinks})


def products(request):
    try:
        products = Product.objects.all()
    except:
        raise Http404("Products not found")
    return render(request, 'cafe/products.html', {"products": products})


def product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except:
        raise Http404("Product not found")
    return render(request, 'cafe/product.html', {"product": product})


def login(request):
    username = request.POST.get('login')
    password = request.POST.get('password')
    users = User.objects.all()
    try:
        user = User.objects.get(login=username, password=password)
    except:
        return render(request, 'cafe/login_failed.html')
    role = user.role
    if role == "barista":
        return render(request, 'cafe/for_barisra.html')
    elif role == "admin":
        return render(request, 'cafe/for_admin.html')
    elif role == "owner":
        return redirect('/baristas/')
