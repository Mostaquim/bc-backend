from datetime import date
from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        max_length=255, unique=True, blank=True, null=True)
    full_name = models.CharField(max_length=130, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateField(auto_now_add=True)
    phone_number_verified = models.BooleanField(default=False)
    change_pw = models.BooleanField(default=True)
    phone_number = models.BigIntegerField(unique=True)
    two_factor_auth = models.BooleanField(default=False)
    address = models.TextField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    class Meta:
        ordering = ('phone_number',)

    def get_short_name(self):
        """
        Returns the display name.
        If full name is present then return full name as display name
        else return username.
        """
        if self.full_name != '':
            return self.full_name
        else:
            return str(self.phone_number)


class OTP_CODES(models.Model):
    phone_number = models.BigIntegerField()
    code = models.CharField(max_length=6)
    date_created = models.DateTimeField(auto_now=True)
    is_used = models.BooleanField(default=False)

    class Meta:
        ordering = ('date_created',)


    def __str__(self):
        return str(self.phone_number)
