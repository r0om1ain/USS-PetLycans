from django.shortcuts import render
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import SpaceAgency, Mission
from .serializers import SpaceAgencySerializer, MissionSerializer

class VaisseauViewSet(viewsets.ModelViewSet):
    queryset = SpaceAgency.objects.all()
    serializer_class = SpaceAgencySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

def tableau_missions(request):
    missions = Mission.objects.filter(
        statut = Mission.STATUT_PROGRAMMEE,
        date_lancement__lte = timezone.now(),
    ).select_related("vaisseau")
    return render(request, "space_agency/tableau.html", {"missions": missions})