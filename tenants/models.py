from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

class School(TenantMixin):
    PLAN_CHOICES = [
        ('free',    'Free Trial'),
        ('starter', 'Starter'),
        ('growth',  'Growth'),
        ('scale',   'Scale'),
    ]
    name           = models.CharField(max_length=200)
    short_name     = models.CharField(max_length=50)
    address        = models.TextField(blank=True)
    phone          = models.CharField(max_length=20, blank=True)
    email          = models.EmailField(blank=True)
    logo           = models.ImageField(upload_to='school_logos/', blank=True)
    principal_name = models.CharField(max_length=100, blank=True)
    plan           = models.CharField(max_length=20, choices=PLAN_CHOICES, default='free')
    is_active      = models.BooleanField(default=True)
    max_students   = models.IntegerField(default=100)
    created_on     = models.DateField(auto_now_add=True)
    auto_create_schema = True

    def __str__(self):
        return f'{self.name} ({self.schema_name})'

class Domain(DomainMixin):
    def __str__(self):
        return self.domain
