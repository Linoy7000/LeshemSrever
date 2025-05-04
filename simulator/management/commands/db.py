import json
import os
from PIL import Image
from django.core.management import BaseCommand
from config.models import Config
from marketing_site.models import Product
from server.globals.constants import TextPosition, DIMENSIONS, ProductCategories
from server.services.storage_service import StorageService
from simulator.helpers import update_img_dimensions
from simulator.models import Element, Type, TrainingData


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.add_products()

    def update_dimensions(self):

        elements = Element.objects.all()
        for i in elements:
            update_img_dimensions(i)

    def store_data_elements(self):
        file_path = "C:/Users/Linoy/Downloads/element.json"
        with open(file_path, 'r') as file:
            data = json.load(file)

        for i in data:
            try:
                Element.objects.create(
                    name=i['name'],
                    price=i['price'],
                    link=i['link'],
                    max_width=i['max_width'],
                    max_height=i['max_height'],
                    vertical_mirror=i['vertical_mirror'],
                    horizontal_mirror=i['horizontal_mirror'],
                    max_stitch_width=i['max_stitch_width'],
                    min_stitch_width=i['max_stitch_height'],
                    text_position=i['text_position'],
                    is_superimposed=i['is_superimposed'],
                    primary_dimensions=i['primary_dimensions'],
                    type=Type.objects.get(id=i['type_id']),
                    height=i['height'],
                    width=i['width'],
                )
            except Exception as e:
                print(e)

    def store_data_training(self):
        file_path = "C:/Users/Linoy/Downloads/trainig.json"
        with open(file_path, 'r') as file:
            data = json.load(file)

        for i in data:
            try:
                TrainingData.objects.create(
                    container_width=i['container_width'],
                    container_height=i['container_height'],
                    position_x=i['position_x'],
                    position_y=i['position_y'],
                    height=i['height'],
                    width=i['width'],
                    element_id=i['element_id'] if i['element_id'] <= 9 else i['element_id'] - 9,
                    product_id=1,
                )
            except Exception as e:
                print(e)

    def update_url(self):

        elements = Element.objects.filter(id__gte=34)

        for i in elements:
            update_img_dimensions(i)
            link = StorageService().upload_image(os.getenv('IMAGES_BASE_URL') + "/" + i.local_link + ".png", f"{i.id}",
                                                 Config.get_config_value('GOOGLE_DRIVE_FOLDERS')['Elements'])
            i.url = link
            i.save()

    def add_elements(self):
        for i in range(47, 53):
            link = StorageService().upload_image(f"{os.getenv('IMAGES_BASE_URL')}/{i}.png", f"{i - 1}",
                                                 Config.get_config_value('GOOGLE_DRIVE_FOLDERS')['Elements'])
            with Image.open(f"{os.getenv('IMAGES_BASE_URL')}/{i}.png").convert('RGBA') as img:
                w, h = img.width, img.height
            try:
                Element.objects.create(
                    local_link=i,
                    url=link,
                    text_position=TextPosition.CENTER,
                    primary_dimensions=DIMENSIONS.HEIGHT,
                    type=Type.objects.get(text_id="DSN"),
                    height=h,
                    width=w,
                )
            except Exception as e:
                print(e)

    def add_products(self):
        id = 6
        p = Product.objects.get(id=id)
        link = StorageService().upload_image(f"{os.getenv('PRODS_BASE_URL')}/{id}.png", f"{id}",
                                             Config.get_config_value('GOOGLE_DRIVE_FOLDERS')['Products'])
        p.link = link
        p.save()
