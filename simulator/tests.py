from django.test import TestCase

from simulator.helpers import get_img_dimensions

from simulator.services.display_service import DisplayService
from simulator.services.simulator_service import Simulator

s = Simulator([1, 33,34, 30, 27, 21, 35], 80, 80, 9).simulate()

DisplayService(80, 80).paste_elements(s)
