from django.db import models
from django.utils.text import slugify
from employee.models import Employee

class Bank(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=100)
    ifsc = models.CharField(max_length=20)
    account_number = models.CharField(max_length=30)
    branch = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug and self.employee:
            base_slug = slugify(self.employee.full_name)
            slug = base_slug
            counter = 1
            while Bank.objects.exclude(id=self.id).filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.full_name} - {self.bank_name}"
