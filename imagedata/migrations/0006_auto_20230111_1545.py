# Generated by Django 3.2 on 2023-01-11 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imagedata', '0005_remove_aadhardata_yob'),
    ]

    operations = [
        migrations.RenameField(
            model_name='aadhardata',
            old_name='is_all_data',
            new_name='netcopy',
        ),
        migrations.AddField(
            model_name='aadhardata',
            name='sex',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
