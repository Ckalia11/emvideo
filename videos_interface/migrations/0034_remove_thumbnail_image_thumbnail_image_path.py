# Generated by Django 4.0.4 on 2022-10-01 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos_interface', '0033_alter_thumbnail_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thumbnail',
            name='image',
        ),
        migrations.AddField(
            model_name='thumbnail',
            name='image_path',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
