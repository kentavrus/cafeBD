from django.db import models


# Create your models here.

class Barist(models.Model):
    ipn = models.CharField("barista's ipn", max_length=20, primary_key=True)
    name = models.CharField("barista's name", max_length=20, null=False)
    surname = models.CharField("barista's surname", max_length=20, null=False)
    phone = models.CharField("barista's phone number", max_length=13, null=False)
    email = models.CharField("barista's email", max_length=20, null=True)
    notes = models.TextField("notes", null=True)

    def __str__(self):
        return "{} {}".format(self.surname, self.name)


class Dish(models.Model):
    name = models.CharField("dish name", max_length=20)
    description = models.TextField("dish description")
    type_of_dish = models.CharField("type of dish", max_length=10)
    margin = models.IntegerField("margin")
    price_for_one = models.IntegerField("price")
    notes = models.TextField("notes", null=True)

    def __str__(self):
        return "{}".format(self.name)
