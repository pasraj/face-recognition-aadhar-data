# Generated by Django 3.2 on 2023-01-12 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imagedata', '0006_auto_20230111_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='pic',
            field=models.FileField(default=None, null=True, upload_to='profile'),
        ),
    ]
