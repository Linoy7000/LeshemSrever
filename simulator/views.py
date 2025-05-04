
from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from marketing_site.models import Product
from simulator.models import Element, TrainingData
from simulator.serializers import ElementSerializer
from simulator.services.perspective_service import PerspectiveService
from simulator.services.resolution import ResolutionService
from simulator.services.simulator_service import Simulator


class ElementViewSet(viewsets.ModelViewSet):
    queryset = Element.objects.all()
    serializer_class = ElementSerializer
    lookup_field = 'uuid'


@api_view(['POST'])
def calc_perspective(request):
    if request.method == 'POST':
        # Access the request body
        data = request.data
        points = data.get('points')
        category = data.get('category')
        dimensions = data.get('dimensions')

        response = PerspectiveService(category, points, dimensions).generate()
        return Response(response, status=status.HTTP_200_OK)


@api_view(['POST'])
def generate_simulation(request):
    if request.method == 'POST':
        # Access the request body
        data = request.data

        elements = data.get('elements')
        width = data.get('width')
        height = data.get('height')
        design = data.get('product')

        # Generate simulation
        elements_data, scale = Simulator([item['id'] for item in elements], int(width), int(height), design).generate()

        response_data = []

        for item in elements_data:
            element_data = item['element_data']
            serialized_element = ElementSerializer(element_data).data
            response_data.append({
                'element_data': serialized_element,
                'id': serialized_element['id'],
                'url': serialized_element['url'],
                'local_link': serialized_element['local_link'],
                'pos_x': item['pos_x'],
                'pos_y': item['pos_y'],
                'width': item['width'],
                'height': item['height']
            })
        response_data = [response_data, scale]
        return Response(response_data, status=status.HTTP_200_OK)


class TrainingView(APIView):
    def post(self, request):
        if request.method == 'POST':
            data = request.data
            items = data.get('simulationsItems')
            container = data.get('container')

            try:
                for item in items:
                    if item:
                        TrainingData.objects.create(
                            product=Product.objects.get(id=int(container['product'])),
                            element=Element.objects.get(local_link=item['local_link']),
                            container_width=container['width'],
                            container_height=container['height'],
                            position_x=(int(item['pos_x']) - int(container['width']) / 2),
                            position_y=(int(item['pos_y']) - int(container['height']) / 2),
                            width=item['width'],
                            height=item['height']
                        )
            except Exception as e:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)


class ResolutionView(APIView):
    def post(self, request):

        if request.method == 'POST' and request.FILES['image']:
            num_colors = request.POST.get('numColors')
            image = request.FILES['image']
            buffer = ResolutionService(image, int(num_colors)).improve_resolution()
            response = HttpResponse(buffer, content_type="image/png")
            response['Content-Disposition'] = 'attachment; filename="improved_image.png"'
            return response
