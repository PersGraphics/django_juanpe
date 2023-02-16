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

def index(request):
    if request.method == 'POST':
        formulario = Formulario(request.POST, request.FILES)
        if formulario.is_valid():
             formulario.save()
        return redirect('panel_imagenes') 
    return render(request, 'django_faces_app/index.html', {'formulario': Formulario()})

def panel_imagenes(request):
    imagenes = Imagenes.objects.all()
    return render(request, 'django_faces_app/panel_imagenes.html', {'imagenes': imagenes})

def imagen(request, id):
    imagen = Imagenes.objects.get(id=id)
    return render(request, 'django_faces_app/imagen.html', {'imagen': imagen})

def aws(request, id):
    imagen = Imagenes.objects.get(id = id)
    session = boto3.Session(region_name='us-west-2')
    rekognition = session.client('rekognition')

    # Cargar imagen
    with open('.' + imagen.archivo.url, 'rb') as imagen_file:
        imagen = imagen_file.read()
    response = rekognition.detect_faces(Image = { 'Bytes': imagen }, Attributes = [ 'ALL' ])
    filtered_faces = filter(lambda face: face["AgeRange"]["Low"] < 18, response['FaceDetails'])
    filtered_faces = list(map(lambda face: face['BoundingBox'], filtered_faces))
    return JsonResponse(filtered_faces, safe = False)

def blur(request, id):
    imagen = Imagenes.objects.get(id = id)
    path = imagen.archivo.path
    csrf_token = get_token(request)
    imagen_ = Image.open(path)
    body = json.loads(request.body)
    coords = body.get('coords')
    for coord in coords:
        x = int(coord['x'])
        y = int(coord['y'])
        w = int(coord['w'])
        h = int(coord['h'])
        region = imagen_.crop((x, y, x + w, y + h))
        region = region.filter(ImageFilter.BLUR)
        imagen_.paste(region, (x, y, x + w, y + h))
    extension = os.path.splitext(path)[1]
    len_extension = len(extension)
    path = path[:-len_extension] + '-blur' + path[-len_extension:]
    imagen_.save(path)
    imagen.archivoBlur = ImageFieldFile(imagen, imagen.archivoBlur, path) 
    imagen.save()

    return render(request, 'django_faces_app/imagen.html', {'imagen': imagen, 'csrf_token': csrf_token})