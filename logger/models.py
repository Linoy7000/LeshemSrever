from django.db import models
from django.utils import timezone


class Log(models.Model):

    # log levels
    INFO = 'info'
    SUCCESS = 'success'
    WARNING = 'warning'
    ERROR = 'error'

    level = models.CharField(choices=(
        (INFO, 'Info'),
        (SUCCESS, 'Success'),
        (WARNING, 'Warning'),
        (ERROR, 'Error'),
    ), max_length=16, default=INFO)

    timestamp = models.DateTimeField(default=timezone.now)
    endpoint = models.CharField(max_length=256, blank=True, null=True)
    object_id = models.CharField(max_length=256, blank=True, null=True)
    payload = models.JSONField(blank=True, null=True)
