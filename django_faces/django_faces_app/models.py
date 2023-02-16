from django.db import models

# Create your models here.
class Imagenes(models.Model):
    archivo = models.ImageField(upload_to='imagenes')
    archivoBlur = models.ImageField(upload_to='imagenes')