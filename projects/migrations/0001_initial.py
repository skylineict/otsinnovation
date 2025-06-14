# Generated by Django 5.2 on 2025-05-22 06:11

import django.db.models.deletion
import shortuuid.django_fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cohorts', '0001_initial'),
        ('courses', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', shortuuid.django_fields.ShortUUIDField(alphabet='abcdefghijklmnqszxcvopl1234567890', editable=False, length=22, max_length=22, prefix='', primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=255)),
                ('instructions', models.TextField()),
                ('deadline', models.DateTimeField()),
                ('max_score', models.PositiveIntegerField()),
                ('project_type', models.CharField(choices=[('individual', 'Individual'), ('cohort', 'Cohort')], max_length=20)),
                ('file', models.FileField(blank=True, null=True, upload_to='project_files/')),
                ('status', models.CharField(choices=[('live', 'Live'), ('finished', 'Finished')], default='live', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('cohorts', models.ManyToManyField(blank=True, related_name='projects', to='cohorts.cohort')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='courses.course')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectSubmission',
            fields=[
                ('id', shortuuid.django_fields.ShortUUIDField(alphabet='abcdefghijklmnqszxcvopl1234567890', editable=False, length=22, max_length=22, prefix='', primary_key=True, serialize=False, unique=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='project_submissions/')),
                ('description', models.TextField(blank=True, null=True)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('score', models.PositiveIntegerField(blank=True, null=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('feedback', models.TextField(blank=True, null=True)),
                ('cohort', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='cohorts.cohort')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='projects.project')),
                ('submitted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_submissions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectAttendance',
            fields=[
                ('id', shortuuid.django_fields.ShortUUIDField(alphabet='abcdefghijklmnqszxcvopl1234567890', editable=False, length=22, max_length=22, prefix='', primary_key=True, serialize=False, unique=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_attendances', to=settings.AUTH_USER_MODEL)),
                ('submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to='projects.projectsubmission')),
            ],
            options={
                'unique_together': {('submission', 'student')},
            },
        ),
    ]
