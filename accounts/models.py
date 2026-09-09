from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models import Model

from accounts.managers import UserManager


class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(max_length=255,unique=True)
    phone_number = models.CharField(max_length=11,unique=True)
    full_name =models.CharField()
    is_active = models.BooleanField(default=True)
    is_admin =models.BooleanField(default= False)
    objects = UserManager()
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email','full_name']

    def __str__(self) -> str:
        return self.email
    def has_perm(self, perm: str, obj: Model | None = ...) -> bool:
        return True
    def has_module_perms(self, app_label: str) -> bool:
        return True
    @property
    def is_staff(self):
        return self.is_admin
class OtpCode(models.Model):
    phone_number=models.CharField()
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now=True)
    def __str__(self) -> str:
        return f'{self.phone_number} - {self.code} - {self.created}'