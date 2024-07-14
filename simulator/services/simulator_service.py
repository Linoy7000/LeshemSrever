
from server.constants import DIMENSIONS, SimulatorConstants
from simulator.models import Element
from simulator.services.training_service import Training


class Simulator:

    def __init__(self, elements_input, container_width, container_height, design):
        self.elements = Element.objects.filter(id__in=elements_input)
        self.container_width = container_width
        self.container_height = container_height
        self.design = design
        self.elements_to_display = []

    def predict(self):
        trainig = Training(self.design)
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
        x, y = self.convert_position_values(element['pos_x'], element['pos_y'], element['width'], element['height'])
        element['pos_x'] = int(x)
        element['pos_y'] = int(y)

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
        left, top = img2['pos_x'], img1['pos_y'] if img1['pos_y'] > img2['pos_y'] else img2['pos_y']
        right, bottom = img1['pos_x'] + img1['width'], img1['pos_y'] + img1['height'] if img1['pos_y'] + img1['height'] < img2['pos_y'] else img2['pos_y'] + img2['height']

    def png_overlap(self):
        pass

    def check_overlap(self):
        sorted_elements_x = sorted(self.elements_to_display, key=lambda x: x['pos_x'])
        sorted_elements_y = sorted(self.elements_to_display, key=lambda x: x['pos_y'])

        for x in range(len(sorted_elements_x) - 1):
            if self.is_overlap(sorted_elements_x[x], sorted_elements_x[x + 1]):
                pass

        for y in range(len(sorted_elements_y) - 1):
            if self.is_overlap(sorted_elements_x[x], sorted_elements_x[x + 1]):
                pass
    def simulate(self):
        self.predict()
        self.mirror()
        print('k')
        for e in self.elements_to_display:
            self.set_aspect_ratio(e)
            self.set_position_values(e)
            self.scale(e)
        return self.elements_to_display
