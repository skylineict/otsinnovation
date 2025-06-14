# Generated by Django 5.2 on 2025-05-22 06:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Mypasscode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passcodeNo', models.CharField(max_length=200, unique=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('courses', models.CharField(max_length=200)),
                ('payment_type', models.CharField(max_length=200)),
                ('date', models.DateField(auto_now_add=True)),
                ('uplaod', models.ImageField(upload_to='payment')),
                ('passcode', models.CharField(max_length=20)),
                ('payment_status', models.CharField(choices=[('pending', 'pending'), ('approved', 'approved'), ('reject', 'reject')], default='pending', max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
