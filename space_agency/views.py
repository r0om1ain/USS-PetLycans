from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

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

    def get_queryset(self):
        queryset = super().get_queryset()
        statut = self.request.query_params.get("statut")
        if statut:
            queryset = queryset.filter(statut=statut)
        return queryset

    @action(detail=True, methods=["patch", "post", "put"], url_path="changer-statut")
    def changer_statut(self, request, id=None):
        serializer = self.get_serializer(
            self.get_object(), data={"statut": request.data.get("statut")}, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


def tableau_missions(request):
    missions = Mission.objects.all().select_related("vaisseau").order_by("-date_lancement")
    return render(request, "space_agency/tableau_missions.html", {"missions": missions})


def tableau_vaisseaux(request):
    vaisseaux = Vaisseau.objects.all().prefetch_related("missions")
    return render(request, "space_agency/tableau_vaisseaux.html", {"vaisseaux": vaisseaux})