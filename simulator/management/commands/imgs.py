import os

from PIL import Image
from django.core.management import BaseCommand


def resize_image(image_path, output_folder, max_size):
    with Image.open(image_path) as img:
        ratio = max_size / max(img.size)
        new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))

        resized_img = img.resize(new_size)

        base_name = os.path.basename(image_path)
        output_path = os.path.join(output_folder, base_name)
        resized_img.save(output_path, format='PNG')


def resize_images_in_folder(input_folder, output_folder, max_size):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        image_path = os.path.join(input_folder, filename)
        if os.path.isfile(image_path):
            resize_image(image_path, output_folder, max_size)


class Command(BaseCommand):

    def handle(self, *args, **options):
        input_folder = "C:/Users/Linoy/Downloads/elements"
        output_folder = "D:/images/elements"
        max_size = 600
        resize_images_in_folder(input_folder, output_folder, max_size)
