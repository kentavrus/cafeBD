from django.http import Http404
from django.shortcuts import render, redirect

from .models import Barist, Dish, Product, Invoice, User, Supplier


# Create your views here.


def baristas(request):
    baristas_list = Barist.objects.all()
    return render(request, 'cafe/owner/baristas_for_owner.html', {"baristas": baristas_list})


def barista_detail(request, barista_ipn):
    try:
        barist = Barist.objects.get(ipn=barista_ipn)
    except:
        raise Http404("Barist not found")
    return render(request, 'cafe/owner/barista_for_owner.html', {"barista": barist})


def index(request):
    return render(request, 'login.html')


def dishes(request):
    try:
        dishes = Dish.objects.all()
    except:
        raise Http404("Dishes not found")
    return render(request, 'cafe/owner/dishes_for_owner.html', {"dishes": dishes})


def dish_detail(request, dish_id):
    try:
        dish = Dish.objects.get(id=dish_id)
    except:
        raise Http404("Dish not found")
    return render(request, 'cafe/owner/dish_for_owner.html', {"dish": dish})


def food(request):
    try:
        foods = Dish.objects.filter(type_of_dish="food")
    except:
        raise Http404("Foods not found")
    return render(request, 'cafe/owner/foods_for_owner.html', {"foods": foods})


def drinks(request):
    try:
        drinks = Dish.objects.filter(type_of_dish="drink")
    except:
        raise Http404("Drinks not found")
    return render(request, 'cafe/owner/drinks_for_owner.html', {"drinks": drinks})


def products(request):
    try:
        products = Product.objects.all()
    except:
        raise Http404("Products not found")
    return render(request, 'cafe/owner/products_for_owner.html', {"products": products})


def product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except:
        raise Http404("Product not found")
    return render(request, 'cafe/owner/product_for_owner.html', {"product": product})


def login(request):
    username = request.POST.get('login')
    password = request.POST.get('password')
    try:
        user = User.objects.get(login=username, password=password)
    except:
        return render(request, 'login.html', {"error": "Login failed"})
    role = user.role
    if role == "barista":
        return render(request, 'cafe/for_barisra.html')
    elif role == "admin":
        return render(request, 'cafe/for_admin.html')
    elif role == "owner":
        return redirect('/owner/')


def suppliers(request):
    try:
        suppliers = Supplier.objects.all()
    except:
        raise Http404("Suppliers not found")
    return render(request, 'cafe/owner/suppliers_for_owner.html', {"suppliers": suppliers})


def supplier_detail(request, supplier_edrpou):
    try:
        supplier = Supplier.objects.get(edrpou=supplier_edrpou)
    except:
        raise Http404("Supplier not found")
    return render(request, 'cafe/owner/supplier_for_owner.html', {"supplier": supplier})


def home(request):
    return render(request, 'cafe/owner/home_for_owner.html')


def add_barist(request):
    return render(request, "cafe/owner/add_barist.html")


def barist_add(request):
    name = request.POST.get('name')
    surname = request.POST.get('surname')
    ipn = request.POST.get('ipn')
    phone = request.POST.get('phone')
    email = request.POST.get('email')
    username = request.POST.get('login')
    password = request.POST.get('password')
    notes = request.POST.get('notes')
    user = User.objects.create(login=username, password=password, role='barista')
    user.save()
    barist = Barist.objects.create(ipn=ipn, name=name, surname=surname, phone=phone, email=email, notes=notes)
    barist.save()
    return redirect("/baristas/")


