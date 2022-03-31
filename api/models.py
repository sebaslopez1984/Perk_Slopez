from django.db import models

# Create your models here.
class Transaccion(models.Model):
    idCompany = models.IntegerField(max_length=10)
    company = models.CharField(max_length=100)
    price = models.IntegerField(max_length=10)
    date = models.CharField(max_length=16)
    status_transaction = models.CharField(max_length=12)
    status_approved = models.CharField(max_length=5)
    
class Empresa(models.Model): 
    Nombre = models.CharField(max_length=100)
    status = models.BooleanField()