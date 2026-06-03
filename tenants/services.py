from django.db import transaction
from django.contrib.auth.models import User
from django_tenants.utils import schema_context
from .models import School, Domain
import re

def slugify_school_name(name):
    slug = name.lower().strip()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'[\s]+', '-', slug)
    return slug[:40].strip('-')

@transaction.atomic
def onboard_new_school(school_name, admin_email, admin_password, plan='free'):
    slug = slugify_school_name(school_name)
    base = slug
    i = 1
    while School.objects.filter(schema_name=slug).exists():
        slug = f'{base}-{i}'; i += 1

    school = School(schema_name=slug, name=school_name, short_name=slug, plan=plan)
    school.save()

    domain = Domain.objects.create(domain=f'{slug}.schoolos.com', tenant=school, is_primary=True)

    with schema_context(slug):
        User.objects.create_superuser('admin', admin_email, admin_password)

    return {
        'schema_name': slug,
        'subdomain':   domain.domain,
        'dashboard':   f'https://{slug}.schoolos.com/admin/',
        'plan':        plan,
    }
