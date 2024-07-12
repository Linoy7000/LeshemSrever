from PIL import Image

SCALE = 4

class DisplayService:

    def __init__(self, height, width):
        self.height = height * SCALE
        self.width = width * SCALE
        self.image = Image.new('RGBA', (int(self.width), int(self.height)), color="black")

    def paste_elements(self, elements):
        for element in elements:
            with Image.open(f"D:/HHH/{element['value']}.png").convert('RGBA') as img:
                w, h = element['width'], img.height * element['width'] / img.width
                img = img.resize((int(w * SCALE), int(h * SCALE)))

                # Calculate the position
                x = self.width / 2 + element['pos_x'] * SCALE - img.width / 2
                y = self.height / 2 + element['pos_y'] * SCALE - img.height / 2

                self.image.paste(img, (int(x), int(y)), img)
        self.image.show()

