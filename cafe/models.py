from django.db import models


# Create your models here.

class Barist(models.Model):
    ipn = models.CharField("barista's ipn", max_length=20, primary_key=True)
    name = models.CharField("barista's name", max_length=20, null=False)
    surname = models.CharField("barista's surname", max_length=20, null=False)
    phone = models.CharField("barista's phone number", max_length=13, null=False)
    email = models.CharField("barista's email", max_length=20, null=True)
    notes = models.TextField("notes", null=False)
