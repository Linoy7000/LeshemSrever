from django.db import models


class Config(models.Model):
    key = models.CharField(max_length=255, blank=False, null=False)
    value = models.JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.key

    @staticmethod
    def get_config_value(key):
        return Config.objects.get(key=key).value

    @staticmethod
    def set_config_value(key, value):
        config = Config.objects.get(key=key)
        config.value = value
        config.save()

    @staticmethod
    def add_config_value(key, sub_key, value):
        config = Config.objects.get(key=key)
        config.value[sub_key] = value
        config.save()
