# Generated by Django 4.0.4 on 2022-05-11 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos_interface', '0013_alter_video_id_delete_random'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show_comments', models.BooleanField()),
            ],
        ),
    ]