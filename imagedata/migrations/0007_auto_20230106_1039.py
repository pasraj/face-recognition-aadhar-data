# Generated by Django 3.2 on 2023-01-06 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imagedata', '0006_auto_20230106_0952'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='address',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='pan_number',
            field=models.CharField(max_length=20, null=True),
        ),
    ]