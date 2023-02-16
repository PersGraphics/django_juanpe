from django.db import models

# Create your models here.
class Imagenes(models.Model):
    file = models.ImageField(upload_to='imagenes')
    bluredfile = models.ImageField(upload_to='imagenes')