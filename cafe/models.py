from django.db import models

# Create your models here.
from django.db.models import Sum


class User(models.Model):
    login = models.CharField("user login name", max_length=20)
    password = models.CharField("user password", max_length=20)
    role = models.CharField("role of user", max_length=20)


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
    margin = models.IntegerField("margin")
    price_for_one = models.IntegerField("price")
    notes = models.TextField("notes for dish", blank=True)

    def __str__(self):
        return "{}".format(self.name)


class Supplier(models.Model):
    edrpou = models.CharField("edrpou of supplier", max_length=30)
    name = models.CharField("name of supplier", max_length=30)
    city = models.CharField("city of supplier", max_length=30)
    street = models.CharField("street of supplier", max_length=30)
    number_of_house = models.CharField("number of house of supplier", max_length=10)
    phone = models.CharField("phone number of supplier", max_length=13)
    email = models.CharField("email of supplier", max_length=30)
    notes = models.TextField("notes for supplier", blank=True)

    @property
    def address(self):
        return u'%s %s %s' % (self.city, self.street, self.number_of_house)

    def __str__(self):
        return "{}".format(self.name)


class Invoice(models.Model):
    date = models.DateTimeField(auto_now_add=True, editable=True)
    name_of_product = models.CharField("name of product in invoice", max_length=30)
    quantity_of_product = models.IntegerField("quantity of product in invoice")
    all_price = models.IntegerField("price for all products", blank=True)
    notes = models.TextField("notes for invoice", blank=True)

    def save(self, *args, **kwargs):
        for i in InvoiceRows.objects.filter(invoice=self):
            self.all_price += i.sum
            self.quantity_of_product += i.quantity_of_product

    def __str__(self):
        return "{} {}".format(self.date, self.name_of_product)


class Product(models.Model):
    name = models.CharField("name of product", max_length=30)
    quantity = models.IntegerField("quantity of product in storage", default=0)
    price_for_kg = models.IntegerField("price for one kg of product")
    notes = models.TextField("notes for product", blank=True)

    def __str__(self):
        return "{}".format(self.name)


class InvoiceRows(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_of_product = models.IntegerField("quantity of product")
    sum = models.IntegerField("sum of one row")

    def save(self, *args, **kwargs):
        self.sum = self.product.price_for_kg * self.quantity_of_product
        super(InvoiceRows, self.save(*args, **kwargs))
