from django.core.management.base import BaseCommand

from server.globals.constants import TextPosition
from simulator.models import Type, Element
from simulator.services.display_service import DisplayService
from simulator.services.editor_service import EditorService
import tkinter as tk

from simulator.services.simulator_service import Simulator
from simulator.services.training_service import Training


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '-c', '--command',
            help='A key value for demonstration purposes'
        )


    def handle(self, *args, **options):

        if options.get('command') == 'editor':
            root = tk.Tk()
            app = EditorService(root, 150, 200)
            root.mainloop()

        elif options.get('command') == 'display':
            container_width = 100
            container_height = 300
            training = Simulator(9)
            values_to_predict = [1, 33,34, 30, 27, 21, 35]
            elements_to_display = []
            for value in values_to_predict:
                try:
                    [pos_x, width], [pos_y, height] = training.predict(width=container_width, height=container_height, element_id=value)
                    elements_to_display.append({
                        'value': Element.objects.get(id=value).link,
                        'pos_x': pos_x,
                        'pos_y': pos_y,
                        'width': width,
                        'height': height
                    })
                except Exception as e:
                    print(e)
            DisplayService(height=container_height, width=container_width).paste_elements(elements_to_display)

        elif options.get('command') == 'train':
            x1_new, x2_new, x3_new = 100, 100, 1
            pred = Training().predict(x1_new, x2_new, x3_new)

            x1_new, x2_new, x3_new = 100, 100, 2
            pred = Training().predict(x1_new, x2_new, x3_new)

            x1_new, x2_new, x3_new = 100, 100, 3
            pred = Training().predict(x1_new, x2_new, x3_new)

            x1_new, x2_new, x3_new = 100, 100, 4
            pred = Training().predict(x1_new, x2_new, x3_new)

        else:
            for _ in range(35,36):
                Element.objects.create(
                    type=Type.objects.get(text_id="PN"),
                    link=f"{_}",
                    text_position=TextPosition.CENTER,
                    primary_dimensions=1
                )
