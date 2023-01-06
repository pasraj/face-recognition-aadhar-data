# Generated by Django 3.2 on 2023-01-06 09:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('imagedata', '0005_adhaar_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='AadharData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('dob', models.CharField(max_length=20, null=True)),
                ('adhar_number', models.CharField(max_length=20, null=True)),
                ('phone_number', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=400, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AadharImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('front_image', models.FileField(upload_to='front')),
                ('back_image', models.FileField(upload_to='back')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('dob', models.CharField(max_length=20, null=True)),
                ('adhar_number', models.CharField(max_length=20, null=True)),
                ('phone_number', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=400, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Adhaar',
        ),
        migrations.DeleteModel(
            name='UserTable',
        ),
        migrations.AddField(
            model_name='aadharimage',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imagedata.userprofile'),
        ),
        migrations.AddField(
            model_name='aadhardata',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imagedata.userprofile'),
        ),
    ]