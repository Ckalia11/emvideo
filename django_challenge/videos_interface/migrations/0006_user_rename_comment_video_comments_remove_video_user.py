# Generated by Django 4.0.4 on 2022-05-09 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos_interface', '0005_alter_video_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('f_name', models.CharField(max_length=200)),
                ('l_name', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
            ],
        ),
        migrations.RenameField(
            model_name='video',
            old_name='comment',
            new_name='comments',
        ),
        migrations.RemoveField(
            model_name='video',
            name='user',
        ),
    ]