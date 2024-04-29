from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import random


def generate_invite_code():
    return ''.join(random.choices('0123456789ABCDEF', k=6))


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The Phone number must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    phone_number = models.CharField(
        'Номер телефона',
        max_length=15,
        unique=True
    )
    invite_code = models.CharField(max_length=6, default=generate_invite_code)
    activated_invite_code = models.CharField(max_length=6, blank=True, null=True)
    

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['invite_code']

    objects = UserManager()

    def __str__(self):
        return self.phone_number