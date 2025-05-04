from io import BytesIO

import cv2
from sklearn.cluster import KMeans
import numpy as np
from PIL import Image


class ResolutionService:

    def __init__(self, image, num_colors):
        self.image = self.convert_to_numpy(image)
        self.num_colors = num_colors

    def convert_to_numpy(self, image):
        image_array = np.frombuffer(image.read(), np.uint8)
        return cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    def improve_resolution(self):

        image = cv2.resize(self.image, None, fx=4, fy=4, interpolation=cv2.HISTCMP_INTERSECT)

        image_array = np.array(image)

        reshaped_array = image_array.reshape(-1, 3)

        reshaped_array = cv2.medianBlur(reshaped_array, 5)

        kmeans = KMeans(n_clusters=self.num_colors)
        kmeans.fit(reshaped_array)
        centers = kmeans.cluster_centers_
        labels = kmeans.labels_
        new_colors = centers[labels].reshape(image_array.shape)
        new_colors = new_colors.astype(np.uint8)
        new_rgb_image = cv2.cvtColor(new_colors.astype(np.uint8), cv2.COLOR_BGR2RGB)
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        new_rgb_image = cv2.filter2D(new_rgb_image, -1, kernel)
        new_image = Image.fromarray(new_rgb_image)

        buffer = BytesIO()
        new_image.save(buffer, format="PNG", quality=90)
        buffer.seek(0)

        return buffer


