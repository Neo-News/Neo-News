from behaviors import Deleteable, TimeStampable
from django.db import models
from django.db import models
# from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)


class UserManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, TimeStampable, Deleteable):
    image = models.TextField(verbose_name=('Profile image'),)
    email = models.EmailField(verbose_name=('Email address'),max_length=255,unique=True,)
    nickname = models.CharField(verbose_name=('Nickname'),max_length=30,unique=True)
    is_active = models.BooleanField(verbose_name=('Is active'),default=False)
    is_staff = models.BooleanField(verbose_name=('Is staff'),default=False)

    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    def __str__(self):
        return self.nickname


class LoginLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='login_log')
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.user} , {self.ip_address}'


class Category(models.Model):
    users = models.ManyToManyField(User, blank=True, related_name='category')
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Keyword(models.Model):
    users = models.ManyToManyField(User, blank=True, related_name='keyword')
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name          















