from django.db import models

# Create your models here.



class Trainingsession(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Livesesion(models.Model):
    status = (
    ('coming soon', 'coming soon'),
    ('live', 'live')
    )
    
    title = models.CharField(max_length=200, blank=True)
    subject = models.CharField(max_length=200, blank=True)
    link    = models.URLField(max_length=300)
    date  =  models.DateField(auto_created=True)
    image =  models.ImageField(upload_to='sesion')
    online  = models.CharField(choices=status, default='coming soon', max_length=300)
    courses = models.ForeignKey(Trainingsession, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.title


class Recapcourse(models.Model):
    name = models.CharField(max_length=200, default=1)
    
    def __str__(self):
        return self.name
    
class Recapsesion(models.Model):
    title = models.CharField(max_length=200)
    link    = models.URLField(max_length=300)
    date  =  models.DateField(auto_created=True)
    image =  models.ImageField(upload_to='sesion')
    courses  =  models.ForeignKey(Recapcourse, on_delete=models.CASCADE,default=1)
    
    def __str__(self):
        return self.title

class Ourteam(models.Model):
    name  = models.CharField(max_length=200)
    files = models.FileField(upload_to='ourteam')
    link = models.URLField()
    