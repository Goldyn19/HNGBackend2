from django.db import models
from .generate import generate_org_id

class Organisation(models.Model):
    orgId = models.CharField(max_length=255, unique=True, default=generate_org_id)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# Create your models here.
