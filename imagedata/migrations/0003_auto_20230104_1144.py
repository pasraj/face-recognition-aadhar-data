# Generated by Django 3.2 on 2023-01-04 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imagedata', '0002_usertable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adhaar',
            name='adhar_number',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='adhaar',
            name='dob',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='adhaar',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='adhaar',
            name='sex',
            field=models.CharField(max_length=20, null=True),
        ),
    ]