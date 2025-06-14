# Generated by Django 5.2 on 2025-05-22 06:11

import django.db.models.deletion
import shortuuid.django_fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Recapcourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=1, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Cohort',
            fields=[
                ('id', shortuuid.django_fields.ShortUUIDField(alphabet='abcdefghijklmnqszxcvopl1234567890', editable=False, length=22, max_length=22, prefix='', primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('whatsapp_link', models.URLField(unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cohort', to='courses.course')),
                ('leader', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='led_cohorts', to=settings.AUTH_USER_MODEL)),
                ('students', models.ManyToManyField(related_name='cohorts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Recapsesion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_created=True)),
                ('title', models.CharField(max_length=200)),
                ('link', models.URLField(max_length=300)),
                ('image', models.ImageField(upload_to='sesion')),
                ('courses', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='cohorts.recapcourse')),
            ],
        ),
        migrations.CreateModel(
            name='CohortLeaderNomination',
            fields=[
                ('id', shortuuid.django_fields.ShortUUIDField(alphabet='abcdefghijklmnqszxcvopl1234567890', editable=False, length=22, max_length=22, prefix='', primary_key=True, serialize=False, unique=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('nomination_reason', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cohort', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leader_nominations', to='cohorts.cohort')),
                ('nominator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nominations_made', to=settings.AUTH_USER_MODEL)),
                ('nominee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nominations_received', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('cohort', 'nominee')},
            },
        ),
    ]
