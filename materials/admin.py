from django.contrib import admin
from.models import Ebooks

# Register your models here.
@admin.register(Ebooks)
class AdminEbook(admin.ModelAdmin):
    list_display = ('name','ebook_files', 'created_at')