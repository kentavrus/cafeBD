from django.db import models

# Create your models here.
from django.db.models import Sum


class User(models.Model):
    login = models.CharField("user login name", max_length=20)
    password = models.CharField("user password", max_length=20)
    role = models.CharField("role of user", max_length=20)
    status = models.BooleanField(default=False)


class Barist(models.Model):
    ipn = models.CharField("barista's ipn", max_length=20, primary_key=True)
    name = models.CharField("barista's name", max_length=20, null=False)
    surname = models.CharField("barista's surname", max_length=20, null=False)
    phone = models.CharField("barista's phone number", max_length=13, null=False)
    email = models.CharField("barista's email", max_length=20, blank=True)
    notes = models.TextField("notes for barista", blank=True)

    def __str__(self):
        return "{} {}".format(self.surname, self.name)


class Dish(models.Model):
    name = models.CharField("dish name", max_length=20)
    description = models.TextField("dish description")
    type_of_dish = models.CharField("type of dish", max_length=10)
    margin = models.FloatField("margin", default=0)
    price_for_one = models.IntegerField("price", default=0)
    notes = models.TextField("notes for dish", blank=True)
    image = models.TextField(default="")

    def __str__(self):
        return "{}".format(self.name)

    def save(self, *args, **kwargs):
        dishrows = DishRows.objects.filter(dish=self)
        print(dishrows)
        for row in dishrows:
            print(row, row.price_for_all_portions)
            self.price_for_one += int(row.price_for_all_portions)
            print(self.price_for_one)
        self.margin = self.price_for_one * 0.1
        self.price_for_one += int(self.margin)
        super(Dish, self).save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField("name of product", max_length=30)
    quantity = models.IntegerField("quantity of product in storage", default=0)
    price_for_kg = models.IntegerField("price for one kg of product")
    notes = models.TextField("notes for product", blank=True)

    def __str__(self):
        return "{}".format(self.name)


class DishRows(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity_of_dish = models.FloatField()
    price_for_all_portions = models.FloatField()

    def save(self, *args, **kwargs):
        print(self.product.price_for_kg, self.quantity_of_dish)
        self.price_for_all_portions = self.product.price_for_kg * self.quantity_of_dish
        super(DishRows, self).save(*args, **kwargs)


class Supplier(models.Model):
    edrpou = models.CharField("edrpou of supplier", max_length=30, unique=True)
    name = models.CharField("name of supplier", max_length=30)
    country = models.CharField("country of supplier", max_length=30, default="Ukraine")
    city = models.CharField("city of supplier", max_length=30)
    street = models.CharField("street of supplier", max_length=30)
    number_of_house = models.CharField("number of house of supplier", max_length=10)
    phone = models.CharField("phone number of supplier", max_length=13)
    email = models.CharField("email of supplier", max_length=30)
    notes = models.TextField("notes for supplier", blank=True, null=True)

    @property
    def address(self):
        return u'%s %s %s %s' % (self.country, self.city, self.street, self.number_of_house)

    def __str__(self):
        return "{}".format(self.name)


class Invoice(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    date = models.DateTimeField(auto_now_add=True, editable=True)
    quantity_of_product = models.IntegerField("quantity of product in invoice")
    all_price = models.IntegerField("price for all products", blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.DO_NOTHING)
    notes = models.TextField("notes for invoice", blank=True)

    def save(self, *args, **kwargs):
        self.quantity_of_product = 0
        self.all_price = 0
        for i in InvoiceRows.objects.filter(invoice_id=self.id):
            self.all_price += i.sum
            self.quantity_of_product += i.quantity_of_product
        super(Invoice, self).save(*args, **kwargs)

    def __str__(self):
        return "{} {}".format(self.date, self.supplier.name)


class InvoiceRows(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_of_product = models.IntegerField("quantity of product")
    sum = models.IntegerField("sum of one row")

    def save(self, *args, **kwargs):
        self.sum = self.product.price_for_kg * self.quantity_of_product
        product = Product.objects.get(id=self.product.id)
        product.quantity += self.quantity_of_product
        print(product.quantity)
        product.save()
        super(InvoiceRows, self).save(*args, **kwargs)


class Card(models.Model):
    quantity_of_bonuses = models.IntegerField("quantity of bonuses on card")


class Bill(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    datetime = models.DateTimeField(auto_now_add=True, editable=True)
    quantity = models.IntegerField("quantity of dishes in bill", default=0)
    price = models.IntegerField("price in bill", default=0)
    card = models.ForeignKey(Card, on_delete=models.DO_NOTHING, blank=True, null=True)
    barist = models.ForeignKey(Barist, on_delete=models.DO_NOTHING)
    barist_name = models.CharField(max_length=30, default="")
    notes = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        self.barist_name = self.barist.surname
        self.price = 0
        self.quantity = 0
        for i in BillRows.objects.filter(bill_id=self.id):
            self.price += i.price
            self.quantity += i.quantity
        super(Bill, self).save(*args, **kwargs)


class BillRows(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.DO_NOTHING)
    bill = models.ForeignKey(Bill, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField("quantity of dish")
    price = models.IntegerField("price of dish", default=0)

    def save(self, *args, **kwargs):
        self.price = self.dish.price_for_one * self.quantity
        super(BillRows, self).save(*args, **kwargs)
