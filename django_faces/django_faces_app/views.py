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

def aws(request, id):
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

def blur(request, id):
    image = Imagenes.objects.get(id = id)
    path = image.file.path
    # print('IMAGE.FILE.PATH -------------------- ', image.bluredfile.path)
    #print('IMAGE.FILE.URL -------------------- ', image.file.url)
    csrf_token = get_token(request)
    img = Image.open(path)
    print(path)
    body = json.loads(request.body)
    
    coords = body.get('coords')
    print('COORDENADAS  -------------------- ', coords)
    
    for coord in coords:
        x = int(coord['x'])
        y = int(coord['y'])
        w = int(coord['w'])
        h = int(coord['h'])
        region = img.crop((x, y, x + w, y + h))
        
        for i in range(0, 40):
            region = region.filter(ImageFilter.BLUR)
        img.paste(region, (x, y, x + w, y + h))
    #print('IMAGE.FILE.PATH -------------------- ', path)
    extension = os.path.splitext(path)[1]
    len_extension = len(extension)

    path = path[:-len_extension] + '-blured' + path[-len_extension:]
    img.save(path)
    image.bluredfile = ImageFieldFile(image, image.bluredfile, path) 
    image.save()
    #print('------------------------------------------- SAVED')

    return render(request, 'django_faces_app/imagen.html', {'imagen': image, 'csrf_token': csrf_token})