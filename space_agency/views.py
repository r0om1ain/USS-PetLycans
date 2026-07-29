from django.shortcuts import render
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Vaisseau, Mission
from .serializers import VaisseauSerializer, MissionSerializer

def home(request):
    return render(request, "base.html", {})


class VaisseauViewSet(viewsets.ModelViewSet):
    queryset = Vaisseau.objects.all()
    serializer_class = VaisseauSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


def tableau_missions(request):
    missions = Mission.objects.all().select_related("vaisseau").order_by("-date_lancement")
    return render(request, "space_agency/tableau_missions.html", {"missions": missions})


def tableau_vaisseaux(request):
    vaisseaux = Vaisseau.objects.all().prefetch_related("missions")
    return render(request, "space_agency/tableau_vaisseaux.html", {"vaisseaux": vaisseaux})