# Generated by Django 4.1.6 on 2023-02-16 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_faces_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagenes',
            name='bluredfile',
            field=models.ImageField(default=' ', upload_to='imagenes'),
            preserve_default=False,
        ),
    ]
