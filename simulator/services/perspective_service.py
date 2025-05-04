import math
import numpy as np
import cv2 as cv

from server.globals.constants import ProductCategories


class PerspectiveService:

    def __init__(self, type, points, dimensions):
        self.type = type
        self.points = points
        self.data = {}
        self.new_points = []
        self.rows = 0
        self.cols = 0
        self.width = dimensions['width'] if dimensions['width'] else None
        self.height = dimensions['height'] if dimensions['height'] else None

    def order_points(self):
        """ Order points - format required in cv2 """
        # 1 2
        # 3 4
        sorted_y = sorted(self.points, key=lambda x: x['y'])
        sorted_x_top = sorted(sorted_y[:2], key=lambda x: x['x'])
        sorted_x_bottom = sorted(sorted_y[2:], key=lambda x: x['x'])
        self.points = sorted_x_top + sorted_x_bottom

    @staticmethod
    def calculate_angle(pt1, pt2) -> float:
        deltaY = pt2['y'] - pt1['y']
        deltaX = pt2['x'] - pt1['x']

        angle_radians = math.atan2(deltaY, deltaX)

        # Convert radians to degrees
        angle_degrees = angle_radians * (180 / math.pi)

        angle_degrees = (angle_degrees + 360) % 360

        return angle_degrees

    @staticmethod
    def calculate_distance(pt1, pt2) -> float:
        distance = math.sqrt((pt2['x'] - pt1['x']) ** 2 + (pt2['y'] - pt1['y']) ** 2)
        return distance

    @staticmethod
    def get_x_distance(pt1, pt2) -> float:
        distance = pt2['x'] - pt1['x']
        return distance

    def generate_perspective_front(self):
        width = self.get_x_distance(self.points[3], self.points[2])
        return {
            'skew': self.calculate_angle(self.points[3], self.points[2]),
            'width': width if width > 0 else -width,
            'height': 50,
            'top': self.points[2]['y'],
            'left': self.points[2]['x'],
            'points': self.points
        }

    def generate_perspective_right(self):
        return {
            'skew': self.calculate_angle(self.points[3], self.points[1]),
            'width': self.get_x_distance(self.points[3], self.points[1]),
            'height': 50,
            'top': self.points[3]['y'],
            'left': self.points[3]['x'],
            'points': self.points
        }

    def generate_perspective_left(self):
        return {
            'skew': self.calculate_angle(self.points[0], self.points[2]),
            'width': self.get_x_distance(self.points[0], self.points[2]),
            'height': 50,
            'top': self.points[0]['y'],
            'left': self.points[0]['x'],
            'points': self.points
        }

    @staticmethod
    def calc_perspective(pts1, pts2):
        return cv.getPerspectiveTransform(pts1, pts2)

    @staticmethod
    def convert_matrix(matrix):
        """ Convert OpenCV matrix to CSS matrix (4x4) """
        return [
            matrix[0, 0], matrix[1, 0], 0, matrix[2, 0],
            matrix[0, 1], matrix[1, 1], 0, matrix[2, 1],
            0, 0, 1, 0,
            matrix[0, 2], matrix[1, 2], 0, matrix[2, 2]
        ]

    def get_edge_values(self, points):
        min_x = min(point['x'] for point in points)
        min_y = min(point['y'] for point in points)
        max_x = max(point['x'] for point in points)
        max_y = max(point['y'] for point in points)

        return min_x, min_y, max_x, max_y

    def get_dimensions(self, points):
        min_x, min_y, max_x, max_y = self.get_edge_values(points)
        width = max_x - min_x
        height = max_y - min_y

        values_to_reduce = {
            'x': min_x,
            'y': min_y
        }
        return width, height, values_to_reduce

    @staticmethod
    def prepare_points_to_perspective(points, values_to_reduce):
        """ Set the left top corner to 0,0 """
        return [list(val - values_to_reduce[key] for key, val in item.items()) for item in points]

    def generate_perspective_main(self):
        self.order_points()

        # Get
        min_x, min_y, max_x, max_y = self.get_edge_values(self.points)
        # Get width, height & values to adjust positions values (left top corner = [0, 0]
        w, h, values_to_reduce = self.get_dimensions(self.points)

        self.rows = h
        self.cols = w
        self.new_points = self.prepare_points_to_perspective(self.points, values_to_reduce)

        pts1 = np.float32([[0, 0], [self.cols, 0], [0, self.rows], [self.cols, self.rows]])
        pts2 = np.float32(self.new_points)

        matrix = self.calc_perspective(pts1, pts2)

        # Convert OpenCV matrix to CSS matrix (4x4)
        matrix_css = self.convert_matrix(matrix)

        css_matrix_str = "matrix3d(" + ",".join(["{:.10e}".format(num) for num in matrix_css]) + ")"
        return {
            'css_matrix_str': css_matrix_str,
            'top': min_y,
            'left': min_x,
            'width': w,
            'height': h,
            'points': self.points
        }

    def generate(self):

        if int(self.type) == ProductCategories.PAROCHET:
            self.data["main"] = self.generate_perspective_main()

        elif int(self.type) == ProductCategories.SEFER_TORA:
            pass

        elif int(self.type) == ProductCategories.BIMA:
            self.data["main"] = self.generate_perspective_main()

            if self.points[1]['x'] > self.points[3]['x']:
                self.data["right"] = self.generate_perspective_right()

            if self.points[2]['x'] > self.points[0]['x']:
                self.data["left"] = self.generate_perspective_left()

            self.data["front"] = self.generate_perspective_front()

        return self.data
