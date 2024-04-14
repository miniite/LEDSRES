# Create your models here
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from location_field.models.plain import PlainLocationField

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a `User` with an email, username, and password."""
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a `User` with all admin permissions."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class UserProfile(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    region = models.CharField(max_length=100)
    parent_company = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'region', 'parent_company']

    def __str__(self):
        return self.email


class Address(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    location = PlainLocationField(based_fields=['city'], zoom=7)

    def __str__(self):
        return f"{self.user.email} {self.city}"


