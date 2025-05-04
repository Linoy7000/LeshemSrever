import os

from PIL import Image

from config.models import Config

SCALE = 4

class DisplayService:

    def __init__(self, width, height):

        self.height = height * SCALE
        self.width = width * SCALE
        self.image = Image.new('RGBA', (int(self.width), int(self.height)))

    def paste_elements(self, elements):
        for element in elements:

            with Image.open(element['url']).convert('RGBA') as img:
                try:
                    img = img.resize((element['width'], element['height']))
                    self.image.paste(img, (element['pos_x'], element['pos_y']), img)
                except ValueError:
                    raise ValueError("Too small, height and width must be > 0")
        self.image.show()

    def editor_paste_elements(self, elements):
        for element in elements:
            with Image.open(f"{os.getenv('IMAGES_BASE_URL')}/{element['id']}.png").convert('RGBA') as img:
                try:
                    img = img.resize((element['width']*SCALE , element['height']*SCALE))
                    self.image.paste(img, ((element['x'] -element['width'] // 2) * SCALE, (element['y'] -element['height'] // 2) * SCALE), img)
                except ValueError:
                    raise ValueError("Too small, height and width must be > 0")
        self.image.show()
        self.save_image(element['id'])

    def save_image(self, id):
        self.image.save(f"{Config.get_config_value('IMAGES_PATH')}{id}.png")

