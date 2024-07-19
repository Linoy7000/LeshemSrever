import cv2
import numpy as np

from server.constants import DIMENSIONS, SimulatorConstants
from simulator.models import Element
from simulator.services.training_service import Training


class Simulator:

    def __init__(self, elements_input, container_width, container_height, design):

        #TODO Optional - handle missing elements elements

        self.elements = Element.objects.filter(id__in=elements_input)
        self.container_width = container_width
        self.container_height = container_height
        self.design = design
        self.elements_to_display = []

    def predict(self):
        trainig = Training(self.design, self.elements.values_list('id', flat=True))
        for e in self.elements:
            [pos_x, width], [pos_y, height] = trainig.predict(self.container_width, self.container_height, e.id)
            self.elements_to_display.append({
                'element_data': e,
                'url': e.get_image_url(),
                'pos_x': pos_x,
                'pos_y': pos_y,
                'width': width,
                'height': height
            })

    def calc_aspect_ratio(self, predicted_width, predicted_height, element_width, element_height, dimension):
        """ Calculate the aspect ratio by the primary dimension """
        if dimension == DIMENSIONS.WIDTH:
            w, h = predicted_width, element_height * predicted_width / element_width

        elif dimension == DIMENSIONS.HEIGHT:
            w, h = element_width * predicted_height / element_height, predicted_height

        return w, h

    def set_aspect_ratio(self, element):
        """ Set aspect ratio values in elements_to_display """
        w, h = self.calc_aspect_ratio(element['width'], element['height'], element['element_data'].width,
                                      element['element_data'].height, element['element_data'].primary_dimensions)
        element['width'] = int(w)
        element['height'] = int(h)

    def convert_position_values(self, pos_x, pos_y, width, height):
        """ Convert position values from an origin-centered axis to top-left origin axis """
        x = self.container_width / 2 + pos_x - width / 2
        y = self.container_height / 2 + pos_y - height / 2
        return x, y

    def set_position_values(self, element):
        """ Set the position values in elements_to_display """
        print('-',element)
        x, y = self.convert_position_values(element['pos_x'], element['pos_y'], element['width'], element['height'])
        element['pos_x'] = int(x)
        element['pos_y'] = int(y)
        print('--', element)

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

    def scale(self, element):
        """ Scaling multiplication """
        element['pos_x'] *= SimulatorConstants.SCALE
        element['pos_y'] *= SimulatorConstants.SCALE
        element['width'] *= SimulatorConstants.SCALE
        element['height'] *= SimulatorConstants.SCALE

    def is_overlap(self, img1, img2):
        return img1['pos_x'] + img1['width'] > img2['pos_x'] or img1['pos_y'] + img1['height'] > img2['pos_y']

    def get_overlap_range(self, img1, img2):
        print(img1, img2)
        left = img1['pos_x'] if img1['pos_x'] > img2['pos_x'] else img2['pos_x']
        top = img1['pos_y'] if img1['pos_y'] > img2['pos_y'] else img2['pos_y']
        right = img1['pos_x'] + img1['width'] if img1['pos_x'] + img1['width'] < img2['pos_x'] + img2['width'] else img2['pos_x'] + img2['width']
        bottom = img1['pos_y'] + img1['height'] if img1['pos_y'] + img1['height'] < img2['pos_y'] + img2['height'] else img2['pos_y'] + img2['height']

        print(top, right, bottom, right)
        return top, right, bottom, left

    def png_overlap(self, img1, img2):
        top, right, bottom, left = self.get_overlap_range(img1, img2)
        print(self.get_overlap_range(img1, img2))
        image1 = cv2.imread(img1['url'], cv2.IMREAD_UNCHANGED)
        image2 = cv2.imread(img2['url'], cv2.IMREAD_UNCHANGED)
        print(top - img1['pos_y'],bottom - img1['pos_y'], left - img1['pos_x'],right - img1['pos_x'])
        print(top - img2['pos_y'],bottom - img2['pos_y'], left - img2['pos_x'],right - img2['pos_x'])
        cropped_img1 = image1[top - img1['pos_y']:bottom - img1['pos_y'], left - img1['pos_x']:right - img1['pos_x']]
        cropped_img2 = image2[top - img2['pos_y']:bottom - img2['pos_y'], left - img2['pos_x']:right - img2['pos_x']]

        alpha1 = cropped_img1[:, :, 3]
        alpha2 = cropped_img2[:, :, 3]

        overlap = np.logical_and(alpha1 > 0, alpha2 > 0)
        print(np.any(overlap))
        return np.any(overlap)

    def check_overlap(self):
        sorted_elements_x = sorted(self.elements_to_display, key=lambda x: x['pos_x'])
        sorted_elements_y = sorted(self.elements_to_display, key=lambda x: x['pos_y'])

        for x in range(len(sorted_elements_x) - 1):
            if self.is_overlap(sorted_elements_x[x], sorted_elements_x[x + 1]):
                self.png_overlap(sorted_elements_x[x], sorted_elements_x[x + 1])

        for y in range(len(sorted_elements_y) - 1):
            if self.is_overlap(sorted_elements_x[y], sorted_elements_x[y + 1]):
                self.png_overlap(sorted_elements_x[y], sorted_elements_x[y + 1])

    def simulate(self):
        self.predict()
        self.mirror()
        print('k')
        for e in self.elements_to_display:
            self.set_aspect_ratio(e)
            self.set_position_values(e)
            self.scale(e)
        # self.check_overlap()
        return self.elements_to_display
