from datetime import timezone, datetime

from django.http import Http404
from django.shortcuts import render, redirect
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Table, TableStyle

from .models import Barist, Dish, Product, Invoice, User, Supplier, Bill, BillRows, InvoiceRows, DishRows

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas


# Create your views here.


def baristas(request):
    baristas_list = Barist.objects.all()
    return render(request, 'cafe/owner/baristas_for_owner.html', {"baristas": baristas_list})


def index(request):
    return render(request, 'login.html')


def dishes(request):
    try:
        dishes = Dish.objects.all()
        user = User.objects.get(status=True)
    except:
        raise Http404("Dishes not found")
    return render(request, 'cafe/owner/dishes_for_owner.html', {"dishes": dishes, "user": user})


def food(request):
    try:
        foods = Dish.objects.filter(type_of_dish="food")
        user = User.objects.get(status=True)
    except:
        raise Http404("Foods not found")
    return render(request, 'cafe/owner/foods_for_owner.html', {"foods": foods, "user": user})


def drinks(request):
    try:
        drinks = Dish.objects.filter(type_of_dish="drink")
        user = User.objects.get(status=True)
    except:
        raise Http404("Drinks not found")
    return render(request, 'cafe/owner/drinks_for_owner.html', {"drinks": drinks, "user": user})


def products(request):
    try:
        products = Product.objects.all()
        suppliers = Supplier.objects.all()
    except:
        raise Http404("Products not found")
    return render(request, 'cafe/owner/products_for_owner.html', {"products": products, "suppliers": suppliers})


def login(request):
    username = request.POST.get('login')
    password = request.POST.get('password')
    try:
        user = User.objects.get(login=username, password=password)
        user.status = True
        user.save()
    except:
        return render(request, 'login.html', {"error": "Login failed"})
    return redirect('/home/')


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
    try:
        user = User.objects.get(status=True)
    except:
        raise Http404("User not found")
    role = user.role
    return render(request, 'cafe/owner/home_for_owner.html', {"role": role})


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
    if dish1_id is not None:
        dishnumber1 = request.POST.get('dishnumber1')
        dish1 = Dish.objects.get(id=dish1_id)
        row1 = BillRows.objects.create(quantity=int(dishnumber1), dish=dish1, bill_id=bill.id)
        row1.save()
        dishrow = DishRows.objects.filter(dish_id=dish1_id)
        for row in dishrow:
            product1 = Product.objects.get(id=row.product_id)
            product1.quantity -= int(dishnumber1) * int(row.quantity_of_dish)
            product1.save()
    dish2_id = request.POST.get('dishname2')
    print(dish2_id)
    if dish2_id is not None:
        dish2 = Dish.objects.get(id=dish2_id)
        dishnumber2 = request.POST.get('dishnumber2')
        row2 = BillRows.objects.create(quantity=int(dishnumber2), dish_id=dish2_id, bill_id=bill.id)
        row2.save()
        dishrow2 = DishRows.objects.filter(dish_id=dish2_id)
        for row in dishrow2:
            product2 = Product.objects.get(id=row.product_id)
            product2.quantity -= int(dishnumber2) * int(row.quantity_of_dish)
            product2.save()
    dish3_id = request.POST.get('dishname3')
    if dish3_id is not None:
        dish3 = Dish.objects.get(id=dish3_id)
        dishnumber3 = request.POST.get('dishnumber3')
        row3 = BillRows.objects.create(quantity=int(dishnumber3), dish_id=dish3_id, bill_id=bill.id)
        row3.save()
        dishrow3 = DishRows.objects.filter(dish_id=dish3_id)
        for row in dishrow3:
            product3 = Product.objects.get(id=row.product_id)
            product3.quantity -= int(dishnumber3) * int(row.quantity_of_dish)
            product3.save()
    notes = request.POST.get('notes')
    bill.notes = notes
    bill.save()
    return redirect('/bills/')


def bills(request):
    try:
        bills = Bill.objects.all().order_by("id")
        user = User.objects.get(status=True)
        barists = Barist.objects.all()
        dishes = Dish.objects.all()
    except:
        raise Http404("Bills not found")
    return render(request, "cafe/owner/bills_for_owner.html",
                  {"bills": bills, "role": user.role, "barists": barists, "dishes": dishes, "vector": 0})


def bill_detail(request, bill_id):
    try:
        bill = Bill.objects.filter(id=bill_id).first()
        billrows = BillRows.objects.filter(bill=bill)
    except:
        raise Http404("Bill not found")
    buffer = io.BytesIO()

    styles = getSampleStyleSheet()
    style = styles["BodyText"]

    p = canvas.Canvas(buffer, pagesize=letter)
    header = Paragraph("<bold><font size=18>Bill " + str(bill.id) + " " + str(
        bill.datetime.strftime("%m/%d/%Y, %H:%M:%S")) + " " + str(
        bill.barist_name) + "</font></bold>", style)
    data = []
    for row in billrows:
        data.append([row.dish.name, row.quantity, row.price])
    t = Table(data)
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                           ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)]))
    data_len = len(data)

    for each in range(data_len):
        if each % 2 == 0:
            bg_color = colors.whitesmoke
        else:
            bg_color = colors.lightgrey
        t.setStyle(TableStyle([('BACKGROUND', (0, each), (-1, each), bg_color)]))
    aW = 540
    aH = 720

    w, h = header.wrap(aW, aH)
    header.drawOn(p, 72, aH)
    aH = aH - h
    w, h = t.wrap(aW, aH)
    t.drawOn(p, 72, aH - h)
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


def add_supplier(request):
    return render(request, "cafe/add/add_supplier.html")


def supplier_add(request):
    edrpou = request.POST.get("edrpou")
    name = request.POST.get("name")
    country = request.POST.get("country")
    city = request.POST.get("city")
    street = request.POST.get("street")
    house = request.POST.get("house")
    phone = request.POST.get("phone")
    email = request.POST.get("email")
    notes = request.POST.get("notes")
    supplier = Supplier.objects.create(edrpou=edrpou, name=name, country=country, city=city, street=street,
                                       number_of_house=house, phone=phone, email=email, notes=notes)
    supplier.save()
    return redirect('/suppliers/')


def invoices(request):
    try:
        invoices = Invoice.objects.all().order_by("id")
        user = User.objects.get(status=True)
        suppliers = Supplier.objects.all()
        products = Product.objects.all()
    except:
        raise Http404("Invoices not found")
    return render(request, "cafe/owner/invoices_owner.html",
                  {"invoices": invoices, "role": user.role, "suppliers": suppliers, "products": products, "vector": 0})


def add_invoice(request):
    try:
        suppliers = Supplier.objects.all()
        products = Product.objects.all()
    except:
        raise Http404("Not found")
    n = range(1, 4)
    return render(request, "cafe/add/add_invoice.html", {"suppliers": suppliers, "products": products, "n": n})


def invoice_add(request):
    supplier_id = request.POST.get("supplier_name")
    try:
        invoice_last = Invoice.objects.all().last()
        invoice = Invoice.objects.create(id=invoice_last.id + 1, supplier_id=supplier_id, date=datetime.now)
    except:
        invoice = Invoice.objects.create(id=0, supplier_id=supplier_id, date=datetime.now)
    product_1 = request.POST.get("product1")
    if product_1 is not None:
        product_number_1 = request.POST.get("productnumber1")
        row1 = InvoiceRows.objects.create(product_id=product_1, invoice=invoice,
                                          quantity_of_product=int(product_number_1) / 2)
        row1.save()
    product_2 = request.POST.get("product2")
    if product_2 is not None:
        product_number_2 = request.POST.get("productnumber2")
        row2 = InvoiceRows.objects.create(product_id=product_2, invoice=invoice,
                                          quantity_of_product=int(product_number_2) / 2)
        row2.save()
    product_3 = request.POST.get("product3")
    if product_3 is not None:
        product_number_3 = request.POST.get("productnumber3")
        row3 = InvoiceRows.objects.create(product_id=product_3, invoice=invoice,
                                          quantity_of_product=int(product_number_3) / 2)
        row3.save()
    notes = request.POST.get("notes")
    invoice.notes = notes
    invoice.save()
    return redirect('/invoices/')


def invoice_detail(request, invoice_id):
    try:
        invoice = Invoice.objects.filter(id=invoice_id).first()
        invoicerows = InvoiceRows.objects.filter(invoice=invoice)
    except:
        raise Http404("Bill not found")
    buffer = io.BytesIO()

    styles = getSampleStyleSheet()
    style = styles["BodyText"]

    p = canvas.Canvas(buffer, pagesize=letter)
    header = Paragraph("<bold><font size=18>Invoice " + str(invoice.id) + " " + str(
        invoice.date.strftime("%m/%d/%Y, %H:%M:%S")) + " " + str(
        invoice.supplier.name) + "</font></bold>", style)
    data = []
    for row in invoicerows:
        data.append([row.product.name, row.quantity_of_product, row.sum])
    t = Table(data)
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                           ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)]))
    data_len = len(data)

    for each in range(data_len):
        if each % 2 == 0:
            bg_color = colors.whitesmoke
        else:
            bg_color = colors.lightgrey
        t.setStyle(TableStyle([('BACKGROUND', (0, each), (-1, each), bg_color)]))
    aW = 540
    aH = 720

    w, h = header.wrap(aW, aH)
    header.drawOn(p, 72, aH)
    aH = aH - h
    w, h = t.wrap(aW, aH)
    t.drawOn(p, 72, aH - h)
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='invoice_' + str(invoice_id) + '.pdf')


def add_dish(request):
    try:
        products = Product.objects.all()
    except:
        raise Http404("Products not found")
    n = range(1, 4)
    return render(request, "cafe/add/add_dish.html", {"products": products, "n": n})


def dish_add(request):
    name = request.POST.get('name')
    description = request.POST.get('description')
    type = request.POST.get('dishtype')
    image = request.POST.get("image")
    notes = request.POST.get('notes')
    try:
        dish_last = Dish.objects.all().last()
        dish = Dish.objects.create(id=dish_last.id + 1, name=name, description=description, type_of_dish=type,
                                   notes=notes, image=image)
    except:
        dish = Dish.objects.create(id=0, name=name, description=description, type_of_dish=type,
                                   notes=notes, image=image)

    dishproduct1 = request.POST.get('dishproduct1')
    if dishproduct1 is not None:
        productnumber1 = request.POST.get('productnumber1')
        row1 = DishRows.objects.create(product_id=dishproduct1, quantity_of_dish=int(productnumber1), dish_id=dish.id)
        row1.save()
    dishproduct2 = request.POST.get('dishproduct2')
    if dishproduct2 is not None:
        productnumber2 = request.POST.get('productnumber2')
        row2 = DishRows.objects.create(product_id=dishproduct2, quantity_of_dish=int(productnumber2), dish_id=dish.id)
        row2.save()
    dishproduct3 = request.POST.get('dishproduct3')
    if dishproduct3 is not None:
        productnumber3 = request.POST.get('productnumber3')
        row3 = DishRows.objects.create(product_id=dishproduct3, quantity_of_dish=int(productnumber3), dish_id=dish.id)
        row3.save()
    dish.save()
    return redirect('/dishes/')


def add_product(request):
    return render(request, "cafe/add/add_product.html")


def product_add(request):
    name = request.POST.get("name")
    price = request.POST.get("price")
    notes = request.POST.get("notes")
    product = Product.objects.create(name=name, price_for_kg=price, notes=notes)
    product.save()
    return redirect('/products/')


def logout(request):
    try:
        user = User.objects.get(status=True)
        user.status = False
        user.save()
    except:
        raise Http404("User not found")
    return redirect('/login/')


def search_bill(request):
    barist_id = request.POST.get('selectBarist')
    dish_id = request.POST.get('selectDish')
    try:
        if barist_id is not None and dish_id is not None:
            bills = Bill.objects.filter(barist_id=barist_id, billrows__dish_id=dish_id)
        elif barist_id is not None:
            bills = Bill.objects.filter(barist_id=barist_id)
        elif dish_id is not None:
            bills = Bill.objects.filter(billrows__dish_id=dish_id)
        user = User.objects.get(status=True)
        barists = Barist.objects.all()
        dishes = Dish.objects.all()
    except:
        raise Http404("Bills not found")
    return render(request, "cafe/owner/bills_for_owner.html",
                  {"bills": bills, "role": user.role, "barists": barists, "dishes": dishes, "vector": 0})


def search_invoices(request):
    supplier_id = request.POST.get('selectSupplier')
    product_id = request.POST.get('selectProduct')
    try:
        if supplier_id is not None and product_id is not None:
            invoices = Invoice.objects.filter(supplier_id=supplier_id, invoicerows__product_id=product_id)
        elif supplier_id is not None:
            invoices = Invoice.objects.filter(supplier_id=supplier_id)
        elif product_id is not None:
            invoices = Invoice.objects.filter(invoicerows__product_id=product_id)
        user = User.objects.get(status=True)
        suppliers = Supplier.objects.all()
        products = Product.objects.all()
    except:
        raise Http404("Invoices not found")
    return render(request, "cafe/owner/invoices_owner.html",
                  {"invoices": invoices, "role": user.role, "suppliers": suppliers, "products": products, "vector": 0})


def delete_dish(request, dish_id):
    dish = Dish.objects.get(id=dish_id)
    dish.delete()
    return redirect("/dishes")


def sort_bills(request, vector):
    try:
        user = User.objects.get(status=True)
        barists = Barist.objects.all()
        dishes = Dish.objects.all()
        if vector == 1:
            return redirect("/bills")
        else:
            bills = Bill.objects.all().order_by("-datetime")
            return render(request, "cafe/owner/bills_for_owner.html",
                          {"bills": bills, "role": user.role, "barists": barists, "dishes": dishes, "vector": 1})
    except:
        raise Http404("Bills not found")


def sort_invoices(request, vector):
    try:
        user = User.objects.get(status=True)
        suppliers = Supplier.objects.all()
        products = Product.objects.all()
        if vector == 1:
            return redirect("/invoices")
        else:
            invoices = Invoice.objects.all().order_by("-date")
            return render(request, "cafe/owner/invoices_owner.html",
                          {"invoices": invoices, "role": user.role, "suppliers": suppliers, "products": products,
                           "vector": 1})
    except:
        raise Http404("Invoices not found")


def search_product(request):
    price = request.POST.get("selectPrice")
    date = request.POST.get("selectDate")
    date_array = date.split("-")
    supplier_id = request.POST.get("selectSupplier")
    funct = request.POST.get("selectFunc")
    suppliers = Supplier.objects.all()
    if funct == "<":
        product = Product.objects.filter(price_for_kg__lte=price, invoicerows__invoice__date__day=date_array[2],
                                         invoicerows__invoice__date__year=date[0],
                                         invoicerows__invoice__date__month=date[1],
                                         invoicerows__invoice__supplier__id=supplier_id)
    elif funct == ">":
        product = Product.objects.filter(price_for_kg__gte=price, invoicerows__invoice__date__day=date_array[2],
                                         invoicerows__invoice__date__year=date_array[0],
                                         invoicerows__invoice__date__month=date_array[1],
                                         invoicerows__invoice__supplier__id=supplier_id)
    return render(request, "cafe/owner/products_for_owner.html", {"products": product, "suppliers": suppliers})


def bills_with_foods_drinks(request):
    try:
        bills = Bill.objects.filter(billrows__dish__type_of_dish="food").filter(billrows__dish__type_of_dish="drink")
        user = User.objects.get(status=True)
        barists = Barist.objects.all()
        dishes = Dish.objects.all()
    except:
        raise Http404("Bills not found")
    return render(request, "cafe/owner/bills_for_owner.html",
                  {"bills": bills, "role": user.role, "barists": barists, "dishes": dishes, "vector": 0})


def quantity_of_bills(request):
    barist_id = request.POST.get("selectBarist")
    date = request.POST.get("selectDate")
    print(date)
    user = User.objects.get(status=True)
    barists = Barist.objects.all()
    dishes = Dish.objects.all()
    if date == "":
        bills_count = Bill.objects.filter(barist_id=barist_id).count()
    elif barist_id != "?":
        date_array = date.split("-")
        print(date_array)
        bills_count = Bill.objects.filter(barist_id=barist_id, datetime__day=date_array[2], datetime__month=date_array[1],
                                          datetime__year=date_array[0]).count()
    barist = Barist.objects.get(ipn=barist_id)
    barist_count = {"barist": barist, "bills_count": bills_count}
    print(barist_count)
    return render(request, "cafe/owner/bills_for_owner.html",
                  {"bills": bills, "role": user.role, "barists": barists, "dishes": dishes, "vector": 0,
                   "barist_count": barist_count})


def get_suppliers(request):
    supplier_id = request.POST.get("selectSupplier")
    s = Supplier.objects.get(id=supplier_id)
    sup =  Supplier.objects.raw("SELECT S.id, S.name FROM cafe_supplier AS S WHERE S.name <> '" + s.name + "' AND NOT EXISTS (SELECT * FROM cafe_invoicerows CNS WHERE CNS.product_id IN (SELECT product_id FROM cafe_invoicerows cns WHERE invoice_id IN (SELECT id FROM cafe_invoice WHERE supplier_id IN (SELECT id FROM cafe_supplier WHERE name = '" + s.name + "'))) AND NOT EXISTS (SELECT * FROM cafe_invoicerows CNS2 WHERE CNS2.product_id = CNS.product_id AND CNS2.product_id IN (SELECT cns2.product_id FROM cafe_invoicerows cns2 WHERE cns2.invoice_id IN  (SELECT cn.id FROM cafe_invoice cn WHERE cn.supplier_id = S.id)) ));")
    suppliers = []
    for i in sup:
        suppliers.append(Supplier.objects.get(id=i.id))
    print(suppliers)
    return render(request, 'cafe/owner/suppliers_for_owner.html', {"suppliers": suppliers})
