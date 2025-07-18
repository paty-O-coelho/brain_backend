from django.shortcuts import render

from rest_framework import viewsets
from .models import Producer, Farm, Harvest, Crop
from .serializers import (
    ProducerSerializer,
    FarmSerializer,
    HarvestSerializer,
    CropSerializer,
)


class ProducerViewSet(viewsets.ModelViewSet):
    queryset = Producer.objects.all()
    serializer_class = ProducerSerializer


class FarmViewSet(viewsets.ModelViewSet):
    queryset = Farm.objects.all()
    serializer_class = FarmSerializer


class HarvestViewSet(viewsets.ModelViewSet):
    queryset = Harvest.objects.all()
    serializer_class = HarvestSerializer


class CropViewSet(viewsets.ModelViewSet):
    queryset = Crop.objects.all()
    serializer_class = CropSerializer
