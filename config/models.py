from django.db import models
from django.db.models import JSONField


class Config(models.Model):
    key = models.CharField(max_length=255, blank=False, null=False)
    value = JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.key
