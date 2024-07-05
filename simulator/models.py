import os

from django.db import models
import uuid

from server.constants import TextPosition


class Type(models.Model):
    name = models.CharField(max_length=50, blank=False)
    text_id = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name} - {self.text_id}"

class Element(models.Model):

    TEXT_POSITION_CHOICES = [
        (TextPosition.BOTTOM, 'BOTTOM'),
        (TextPosition.RIGHT, 'RIGHT'),
        (TextPosition.LEFT, 'LEFT'),
        (TextPosition.CENTER, 'CENTER'),
        (TextPosition.TOP, 'TOP')
    ]

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    link = models.CharField(max_length=255, blank=False, null=False)
    max_width = models.FloatField(blank=True, null=True)
    max_height = models.FloatField(blank=True, null=True)
    vertical_mirror = models.BooleanField(default=False)
    horizontal_mirror = models.BooleanField(default=False)
    max_stitch_width = models.FloatField(blank=True, null=True)
    max_stitch_height = models.FloatField(blank=True, null=True)
    text_position = models.PositiveIntegerField(choices=TEXT_POSITION_CHOICES)
    is_superimposed = models.BooleanField(default=False)

    def get_image_url(self):
        base_url = os.getenv('IMAGES_BASE_URL')
        return f"{base_url}/{self.id}.png"

    def __str__(self):
        return f"{self.type} - {self.id}"


class TrainingData(models.Model):
    element = models.ForeignKey(Element, on_delete=models.CASCADE)
    container_width = models.IntegerField(blank=False, null=False)
    container_height = models.IntegerField(blank=False, null=False)
    position_x = models.FloatField(blank=False, null=False)
    position_y = models.FloatField(blank=False, null=False)
    width = models.FloatField(blank=False, null=False)
    height = models.FloatField(blank=False, null=False)

    def __str__(self):
        return f"{int(self.container_width)}/{int(self.container_height)} | {self.element}"
