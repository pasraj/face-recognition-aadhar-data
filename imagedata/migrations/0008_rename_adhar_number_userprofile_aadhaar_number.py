# Generated by Django 3.2 on 2023-01-12 08:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imagedata', '0007_userprofile_pic'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='adhar_number',
            new_name='aadhaar_number',
        ),
    ]
