import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'portal.settings')
django.setup()

from registration.models import MyUser

# Check if the superuser already exists
if not MyUser.objects.filter(username='admin').exists():
    # Create a superuser
    user = MyUser.objects.create_superuser(
        username='admin',
        phone='08101524926',
        password='admin'
    )
    print('Superuser created successfully!')
else:
    print('Superuser already exists.')
