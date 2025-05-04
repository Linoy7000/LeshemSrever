from django.urls import path, include
from rest_framework.routers import DefaultRouter
from simulator.views import ElementViewSet, generate_simulation, calc_perspective, ResolutionView, \
    TrainingView

router = DefaultRouter()
router.register(r'elements', ElementViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('generate/', generate_simulation),
    path('perspective/', calc_perspective),
    path('resolution/', ResolutionView.as_view()),
    path('train/', TrainingView.as_view())
]

