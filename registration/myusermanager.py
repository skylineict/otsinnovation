from django.contrib.auth.models import BaseUserManager



class Usermanager(BaseUserManager):
    def create_user(self, phone, username, password=None, **extra_fields):
        if not phone:
            raise ValueError("Users must have phone number")
        user = self.model(phone=phone, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    #  Creates and saves a User with the given phone and password.
    
    
    def create_staffuser(self, phone, username, password=None,**extra_fields):
          #Creates and saves a staff user with the given email and password.
          user = self.create_user(phone, username, password **extra_fields)
          user.is_staff = True
          user.save(using=self._db)
          return user
      
    def create_superuser(self, phone, username, password=None, **extra_fields):
        
        #Creates and saves a superuser with the given email and password.
        user = self.create_user(phone, username, password,**extra_fields)
        user.is_staff = True
        user.is_admin  = True
        user.save(using=self._db)
        return user