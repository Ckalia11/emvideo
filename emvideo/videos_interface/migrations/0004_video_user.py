# Generated by Django 4.0.4 on 2022-05-09 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos_interface', '0003_remove_video_comments_video_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='user',
            field=models.CharField(default='ckalia', max_length=100),
            preserve_default=False,
        ),
    ]