import io

import numpy as np
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
import cv2 as cv
from rest_framework.decorators import api_view


@api_view(['POST'])
def calc_prespective(request):

    if request.method == 'POST':
        # Access the request body
        data = request.data
        points = data.get('points')
        product = data.get('product')

        if points and product:
            print(points)


            # Clockwise order
            # if not (points[0]['y'] <= points[3]['y'] and points[0]['x'] >= points[3]['x']):
            #     points.reverse()

            # Swap elements at index 2 and index 3 - adjust to the indexes below
            # 1 # 2 #
            # 3 # 4 #
            points[2], points[3] = points[3], points[2]

            # Calc position
            min_x = min(point['x'] for point in points)
            min_y = min(point['y'] for point in points)
            max_x = max(point['x'] for point in points)
            max_y = max(point['y'] for point in points)
            print(min_x, min_y, max_x, max_y)
            values_to_reduce = {
                'x': min_x,
                'y': min_y
            }
            w = max_x - min_x
            h = max_y - min_y
            img = cv.imread('C:/Users/Linoy/project/client/app/src/' + product)
            assert img is not None, "file could not be read, check with os.path.exists()"
            resized_img = cv.resize(img, (w, h), interpolation=cv.INTER_AREA)

            rows, cols, ch = img.shape
            converted_points = [list(val - values_to_reduce[key] for key, val in item.items()) for item in points]

            pts1 = np.float32([[0, 0], [cols, 0], [0, rows], [cols, rows]])
            pts2 = np.float32(converted_points)

            M = cv.getPerspectiveTransform(pts1, pts2)

            matrix = cv.getPerspectiveTransform(pts1, pts2)

            # Convert OpenCV matrix to CSS matrix (4x4)
            matrix_css = [
                matrix[0, 0], matrix[1, 0], 0, matrix[2, 0],
                matrix[0, 1], matrix[1, 1], 0, matrix[2, 1],
                0, 0, 1, 0,
                matrix[0, 2], matrix[1, 2], 0, matrix[2, 2]
            ]
            css_matrix_str = "matrix3d(" + ",".join(["{:.10e}".format(num) for num in matrix_css]) + ")"

            dst = cv.warpPerspective(img, M, (cols, rows))

            retval, buffer = cv.imencode('.jpg', dst)
            cv.imshow('k', dst)
            cv.waitKey(0)  # Waits indefinitely for a key press
            cv.destroyAllWindows()  # Closes all OpenCV windows
            return Response({
                'css_matrix_str': css_matrix_str,
                'top': min_y,
                'left': min_x,
                'width': max_x - min_x,
                'height': max_y - min_y,
                'center_x': w/2 + min_x,
                'canter_y': h/2 + min_y
            }, status=status.HTTP_200_OK)

        return Response({'error': 'Error'}, status=status.HTTP_400_BAD_REQUEST)
