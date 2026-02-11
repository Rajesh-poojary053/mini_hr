from django.db import models
from django.conf import settings
from django.utils.text import slugify
from employee.models import Employee

DOCUMENT_CHOICES = [
    ('Aadhar Card', 'Aadhar Card'),
    ('PAN Card', 'PAN Card'),
    ('Education Certificate', 'Education Certificate'),
]

class Document(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=50, choices=DOCUMENT_CHOICES)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.employee.full_name}-{self.document_type}")
            slug = base_slug
            counter = 1
            while Document.objects.exclude(id=self.id).filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.full_name} - {self.document_type}"
