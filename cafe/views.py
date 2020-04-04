from datetime import timezone, datetime

from django.http import Http404
from django.shortcuts import render, redirect

from .models import Barist, Dish, Product, Invoice, User, Supplier, Bill, BillRows

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas


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
    return render(request, "cafe/add/add_barist.html")


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


def bill_add(request):
    barist_id = request.POST.get('baristname')
    barist = Barist.objects.get(ipn=barist_id)
    try:
        bill_last = Bill.objects.all().last()
        bill = Bill.objects.create(id=bill_last.id + 1, barist=barist, datetime=datetime.now)
    except:
        bill = Bill.objects.create(id=0, barist=barist, datetime=datetime.now)
    dish1_id = request.POST.get('dishname1')
    print(dish1_id)
    if dish1_id is not None:
        dishnumber1 = request.POST.get('dishnumber1')
        dish1 = Dish.objects.get(id=dish1_id)
        row1 = BillRows.objects.create(quantity=int(dishnumber1), dish=dish1, bill_id=bill.id)
        row1.save()
    dish2_id = request.POST.get('dishname2')
    print(dish2_id)
    if dish2_id is not None:
        dish2 = Dish.objects.get(id=dish2_id)
        dishnumber2 = request.POST.get('dishnumber2')
        row2 = BillRows.objects.create(quantity=int(dishnumber2), dish_id=dish2_id, bill_id=bill.id)
        row2.save()
    dish3_id = request.POST.get('dishname3')
    if dish3_id is not None:
        dish3 = Dish.objects.get(id=dish3_id)
        dishnumber3 = request.POST.get('dishnumber3')
        row3 = BillRows.objects.create(quantity=int(dishnumber3), dish_id=dish3_id, bill_id=bill.id)
        row3.save()
    notes = request.POST.get('notes')
    bill.notes = notes
    bill.save()
    return redirect('/bills/')


def bills(request):
    try:
        bills = Bill.objects.all()
    except:
        raise Http404("Bills not found")
    return render(request, "cafe/owner/bills_for_owner.html", {"bills": bills})


def bill_detail(request, bill_id):
    try:
        bill = Bill.objects.filter(id=bill_id).first()
        billrows = BillRows.objects.filter(bill=bill)
    except:
        raise Http404("Bill not found")
    buffer = io.BytesIO()

    p = canvas.Canvas(buffer)
    width, height = 595.27, 841.89

    p.drawString(10, height - 10, str(bill.id))
    p.drawString(15, height - 15, bill.barist_name)
    for row in billrows:
        i = 25
        p.drawString(100, height - i, row.dish.name)
        p.drawString(400, height - i, str(row.quantity))
        p.drawString(600, height - i, str(row.price))
        i += 10
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='bill_' + str(bill_id) + '.pdf')


def add_bill(request):
    try:
        baristas = Barist.objects.all()
        dishes = Dish.objects.all()
    except:
        Http404("Barists not found")
    n = range(1, 4)
    return render(request, 'cafe/add/bill_add.html', {"baristas": baristas, "n": n, "dishes": dishes})
