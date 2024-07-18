from django.contrib import admin

from simulator.models import Type, Element, TrainingData

# Simulator
admin.site.register(Type)
admin.site.register(Element)
admin.site.register(TrainingData)
