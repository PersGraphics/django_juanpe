from django.shortcuts import render

from django.shortcuts import render, redirect
from .forms import Formulario
from .models import Imagenes
from django.http import JsonResponse
from django.http import HttpResponse
import boto3 # Instalar en consola
import json
from django.middleware.csrf import get_token
from PIL import Image, ImageFilter
from django.core.cache import cache
from django.db.models.fields.files import ImageFieldFile
import os

# CAMBIAR NOMBRE VARIABLES ETC

def index(request):
    if request.method == 'POST':
        form = Formulario(request.POST, request.FILES)
        if form.is_valid():
             object = form.save()
        return redirect('panel_imagenes') # cambiar a pagina nombre

    return render(request, 'django_faces_app/index.html', {'form': Formulario()})


def panel_imagenes(request):
    pictures = Imagenes.objects.all()
    return render(request, 'django_faces_app/panel_imagenes.html', {'imagenes': pictures})


def imagen(request, id):
    imagen = Imagenes.objects.get(id=id)
    return render(request, 'django_faces_app/imagen.html', {'imagen': imagen})

def aws(request):
    pic = Imagenes.objects.get(id = id)
    session = boto3.Session(region_name='us-west-2')
    rekognition = session.client('rekognition')

    # Cargar imagen
    with open('.' + pic.file.url, 'rb') as image_file:
        image = image_file.read()
    response = rekognition.detect_faces(Image = { 'Bytes': image }, Attributes = [ 'ALL' ])
    filtered_faces = filter(lambda face: face["AgeRange"]["Low"] < 18, response['FaceDetails'])
    filtered_faces = list(map(lambda face: face['BoundingBox'], filtered_faces))
    return JsonResponse(filtered_faces, safe = False)