# Generated by Django 4.0.4 on 2022-12-27 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos_interface', '0038_rename_image_path_thumbnail_image_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thumbnail',
            name='image_file',
            field=models.ImageField(upload_to='', verbose_name=''),
        ),
    ]