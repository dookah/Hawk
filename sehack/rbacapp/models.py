from django.db import models

# Create your models here.

class Integration(models.Model):
    user = models.CharField(max_length=200)
    product = models.CharField(max_length=50)
    host = models.CharField(max_length=200)
    ikey = models.CharField(max_length=200)
    skey = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)