# Generated by Django 4.0.4 on 2022-05-27 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos_interface', '0027_remove_thumbnail_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='thumbnail',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/', verbose_name=''),
        ),
    ]
