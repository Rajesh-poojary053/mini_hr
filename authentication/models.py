# ✅ authentication/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.conf import settings

class CompanyUserManager(BaseUserManager):
    def create_user(self, email, company_name, hr_name, mobile, password=None):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            company_name=company_name,
            hr_name=hr_name,
            mobile=mobile
        )
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, company_name, hr_name, mobile, password=None):
        user = self.create_user(email, company_name, hr_name, mobile)
        user.is_verified = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user

class CompanyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    company_name = models.CharField(max_length=100)
    hr_name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    otp = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['company_name', 'hr_name', 'mobile']

    objects = CompanyUserManager()

    def __str__(self):
        return f"{self.email} - {self.company_name}"

# authentication/models.py

class OTP(models.Model):
    email = models.EmailField(default='default@example.com')  # ✅ instead of linking to user
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        from django.utils import timezone
        return (timezone.now() - self.created_at).seconds < 300

    def __str__(self):
        return f"{self.email} - {self.code}"
