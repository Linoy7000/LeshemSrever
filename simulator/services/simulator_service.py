import copy

import cv2
import matplotlib.pyplot as plt
import numpy as np

from config.models import Config
from logger.models import Log
from server.globals.constants import DIMENSIONS, SimulatorConstants, LogLevel
from simulator.models import Element, Type
from simulator.services.training_service import Training


class Simulator:

    def __init__(self, elements_input, container_width, container_height, design):

        self.elements = (
            Element.objects.filter(id__in=elements_input) |
            Element.objects.filter(type__in=Type.objects.filter(text_id__in=['PSK', 'CTV']))
        )
        self.container_width = container_width
        self.container_height = container_height
        self.design = design
        self.elements_to_display = []

    def predict(self):

        trainig = Training(self.design, self.elements.values_list('id', flat=True))

        if trainig:
            for e in self.elements:
                [pos_x, width], [pos_y, height] = trainig.predict(self.container_width, self.container_height, e.id)

                self.elements_to_display.append({
                    'element_data': e,
                    'url': e.get_image_url(),
                    'pos_x': int(pos_x),
                    'pos_y': int(pos_y),
                    'width': int(width),
                    'height': int(height)
                })
        else:
            for e in self.elements:
                self.elements_to_display.append({
                    'element_data': e,
                    'url': e.get_image_url(),
                    'pos_x': 0,
                    'pos_y': 0,
                    'width': 50,
                    'height': 50
                })

    def calc_aspect_ratio(self, predicted_width, predicted_height, element_width, element_height, dimension):
        """ Calculate the aspect ratio by the primary dimension """
        if dimension == DIMENSIONS.WIDTH:
            w, h = predicted_width, element_height * predicted_width / element_width

        elif dimension == DIMENSIONS.HEIGHT:
            w, h = element_width * predicted_height / element_height, predicted_height

        return int(w), int(h)

    def set_aspect_ratio(self, image=None):
        """ Set aspect ratio values in elements_to_display """
        if image:
            w, h = self.calc_aspect_ratio(image['width'], image['height'], image['element_data'].width,
                                          image['element_data'].height, image['element_data'].primary_dimensions)
            image['width'] = int(w)
            image['height'] = int(h)
            return

        for element in self.elements_to_display:
            w, h = self.calc_aspect_ratio(element['width'], element['height'], element['element_data'].width,
                                          element['element_data'].height, element['element_data'].primary_dimensions)
            element['width'] = int(w)
            element['height'] = int(h)

    def convert_position_values(self, pos_x, pos_y, width, height):
        """ Convert position values from an origin-centered axis to top-left origin axis """
        x = self.container_width / 2 + pos_x
        y = self.container_height / 2 + pos_y
        return x, y

    def set_position_values(self):
        """ Set the position values in elements_to_display """
        clone_elements = self.elements_to_display.copy()
        for element in clone_elements:
            x, y = self.convert_position_values(element['pos_x'], element['pos_y'], element['width'], element['height'])
            element['pos_x'] = int(x)
            element['pos_y'] = int(y)
        return clone_elements

    def convert_position_values_by_size(self, pos_x, pos_y, width, height):
        """ Convert position values from an origin-centered axis to top-left origin axis """
        x = self.container_width / 2 + pos_x - width / 2
        y = self.container_height / 2 + pos_y - height / 2

        return x, y

    def set_position_values_by_size(self):
        """ Set the position values in elements_to_display """
        clone_elements = copy.deepcopy(self.elements_to_display)
        for element in clone_elements:
            x, y = self.convert_position_values_by_size(element['pos_x'], element['pos_y'], element['width'], element['height'])
            element['pos_x'] = int(x)
            element['pos_y'] = int(y)

        return clone_elements

    def mirror(self):
        """ Add mirror to element if needed """
        values = []
        for e in self.elements_to_display:

            if e['element_data'].vertical_mirror:
                values.append({
                    'element_data': e['element_data'],
                    'url': e['element_data'].get_image_url(),
                    'pos_x': e['pos_x'] * -1,
                    'pos_y': e['pos_y'],
                    'width': e['width'],
                    'height': e['height']
                })

            elif e['element_data'].horizontal_mirror:
                values.append({
                    'element_data': e['element_data'],
                    'url': e['element_data'].get_image_url(),
                    'pos_x': e['pos_x'],
                    'pos_y': e['pos_y'] * -1,
                    'width': e['width'],
                    'height': e['height']
                })
        # Add to elements_to_display
        for val in values:
            self.elements_to_display.append(val)

    def calc_scale(self):
        client_width = 565
        client_height = 500
        width_ratio = client_width / self.container_width
        height_ratio = client_height / self.container_height
        return min(width_ratio, height_ratio)

    def scale(self, multiplier=None, env="client"):
        """ Scaling multiplication """

        if multiplier:
            scale = multiplier

        else:
            if env == 'server':
                scale = Config.get_config_value('LOCAL_SCALE')
            else:
                scale = Config.get_config_value('CLIENT_SCALE')

        for element in self.elements_to_display:
            element['pos_x'] *= scale
            element['pos_y'] *= scale
            element['width'] *= scale
            element['height'] *= scale

    def is_overlap(self, img1, img2, axis=None):
        condition_x1 = img1['pos_x'] + img1['width'] > img2['pos_x']
        condition_y1 = img1['pos_y'] + img1['height'] > img2['pos_y']
        condition_x2 = img2['pos_x'] + img2['width'] > img1['pos_x']
        condition_y2 = img2['pos_y'] + img2['height'] > img1['pos_y']

        return (condition_x1 if img1['pos_x'] < img2['pos_x'] else condition_x2) and (
            condition_y1 if img1['pos_y'] < img2['pos_y'] else condition_y2)

    def get_overlap_range(self, img1, img2):
        left = img1['pos_x'] if img1['pos_x'] > img2['pos_x'] else img2['pos_x']
        top = img1['pos_y'] if img1['pos_y'] > img2['pos_y'] else img2['pos_y']
        right = img1['pos_x'] + img1['width'] if img1['pos_x'] + img1['width'] < img2['pos_x'] + img2['width'] else \
        img2['pos_x'] + img2['width']
        bottom = img1['pos_y'] + img1['height'] if img1['pos_y'] + img1['height'] < img2['pos_y'] + img2['height'] else \
        img2['pos_y'] + img2['height']

        return top, right, bottom, left

    def png_overlap(self, img1, img2):
        top, right, bottom, left = self.get_overlap_range(img1, img2)

        image1 = cv2.imread(img1['url'], cv2.IMREAD_UNCHANGED)
        image2 = cv2.imread(img2['url'], cv2.IMREAD_UNCHANGED)

        image1 = cv2.resize(image1, (int(img1['width']), int(img1['height'])))
        image2 = cv2.resize(image2, (int(img2['width']), int(img2['height'])))

        cropped_img1 = image1[int(top - img1['pos_y']):int(bottom - img1['pos_y']),
                       int(left - img1['pos_x']):int(right - img1['pos_x'])]
        cropped_img2 = image2[int(top - img2['pos_y']):int(bottom - img2['pos_y']),
                       int(left - img2['pos_x']):int(right - img2['pos_x'])]

        alpha1 = cropped_img1[:, :, 3]
        alpha2 = cropped_img2[:, :, 3]

        overlap = np.logical_and(alpha1 > 0, alpha2 > 0)

        indices = np.argwhere(overlap)

        if indices.size > 0:
            min_y, min_x = indices.min(axis=0)  # קצה שמאלי עליון
            max_y, max_x = indices.max(axis=0)

        return [np.any(overlap), (max_x - min_x, max_y - min_y)]

    def check_overlap(self):
        elements_count = self.elements_to_display.__len__()
        cloned_elements = self.set_position_values_by_size()
        for i in range(elements_count):
            for j in range(i + 1, elements_count):
                if cloned_elements[i]['element_data'].local_link in ['37', '41'] or cloned_elements[j]['element_data'].local_link in ['37', '41']:
                    return
                if self.is_overlap(cloned_elements[i], cloned_elements[j]):
                    overlap, (w, h) = self.png_overlap(cloned_elements[i], cloned_elements[j])
                    if overlap:
                        pass
                        # self.adjust_elements(self.elements_to_display[i], self.elements_to_display[j], size=(w, h))

    def adjust_elements(self, img1, img2, size):
        overlap_width = size[0]
        overlap_height = size[1]

        try:
            if overlap_width < overlap_height:
                diff = (img1['width'] - (overlap_width // 2 + 1)) / img1['width']

                img1['width'] *= diff
                img1['height'] *= diff
                diff2 = (img2['width'] - (overlap_width // 2 +1)) / img2['width']

                img2['width'] *= diff2
                img2['height'] *= diff2

            else:
                diff = (img1['height'] - (overlap_height // 2 +1)) / img1['height']
                img1['width'] *= diff
                img1['height'] *= diff
                diff2 = (img2['height'] - (overlap_height // 2 + 1)) / img2['height']

                img2['width'] *= diff2
                img2['height'] *= diff2
        except Exception as e:
            Log.objects.create(
                level=LogLevel.ERROR,
                payload={"messgae": str(e)}
            )

    def generate(self, env='client'):
        self.predict()
        self.check_overlap()
        self.mirror()
        self.set_aspect_ratio()
        self.elements_to_display = self.set_position_values()
        scale = self.calc_scale()
        self.scale(scale)
        return self.elements_to_display, scale
