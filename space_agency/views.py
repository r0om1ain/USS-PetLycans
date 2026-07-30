from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Vaisseau, Mission, Lieu
from .serializers import VaisseauSerializer, MissionSerializer, LieuSerializer
from .trajets import optimiser_trajet, resultat_en_dict


def home(request):
    return render(request, "base.html", {})


class VaisseauViewSet(viewsets.ModelViewSet):
    queryset = Vaisseau.objects.all()
    serializer_class = VaisseauSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def _missions_actives(self, vaisseau):
        """Récupère dynamiquement les missions encore à faire pour ce vaisseau."""
        missions = Mission.objects.filter(
            vaisseau=vaisseau,
            statut__in=[Mission.STATUT_PROGRAMMEE, Mission.STATUT_EN_COURS],
        ).order_by("date_lancement")
        return list(missions)

    @action(
        detail=True,
        methods=["get"],
        url_path="optimiser-trajet",
        permission_classes=[AllowAny],
    )
    def optimiser_trajet_vaisseau(self, request, pk=None):
        """
        Pour UN vaisseau :
        1. récupère ses missions existantes
        2. ajoute des coordonnées fictives si besoin
        3. calcule le meilleur ordre de déplacement
        """
        vaisseau = self.get_object()
        missions = self._missions_actives(vaisseau)

        if len(missions) == 0:
            return Response(
                {
                    "vaisseau_id": vaisseau.id,
                    "vaisseau": vaisseau.nom,
                    "ordre": [],
                    "distance_totale": 0,
                    "etapes": [],
                    "detail": "Aucune mission active pour ce vaisseau.",
                }
            )

        resultat = optimiser_trajet(missions)
        return Response(resultat_en_dict(vaisseau, resultat))

    @action(
        detail=False,
        methods=["get"],
        url_path="optimiser-trajets",
        permission_classes=[AllowAny],
    )
    def optimiser_trajets(self, request):
        """
        Pour TOUS les vaisseaux :
        récupère les missions de chacun et optimise leurs déplacements.
        """
        tous_les_resultats = []

        for vaisseau in Vaisseau.objects.all():
            missions = self._missions_actives(vaisseau)
            resultat = optimiser_trajet(missions)
            tous_les_resultats.append(resultat_en_dict(vaisseau, resultat))

        return Response(tous_les_resultats)


class LieuViewSet(viewsets.ModelViewSet):
    queryset = Lieu.objects.all()
    serializer_class = LieuSerializer
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
    def changer_statut(self, request, pk=None):
        serializer = self.get_serializer(
            self.get_object(), data={"statut": request.data.get("statut")}, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=["get"], url_path="distance")
    def distance(self, request, pk=None):
        mission = self.get_object()
        vers_id = request.query_params.get("vers")

        if vers_id is None:
            return Response(
                {"detail": "Il faut donner ?vers=id_de_la_mission"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            autre = Mission.objects.get(pk=vers_id)
        except Mission.DoesNotExist:
            return Response(
                {"detail": "Mission introuvable."},
                status=status.HTTP_404_NOT_FOUND,
            )

        dist = mission.destination.distance_vers(autre.destination)

        return Response(
            {
                "distance": dist,
                "de": mission.destination.nom,
                "vers": autre.destination.nom,
            }
        )


def tableau_missions(request):
    missions = Mission.objects.all().order_by("-date_lancement")
    return render(
        request, "space_agency/tableau_missions.html", {"missions": missions}
    )


def tableau_vaisseaux(request):
    vaisseaux = Vaisseau.objects.all()
    return render(
        request, "space_agency/tableau_vaisseaux.html", {"vaisseaux": vaisseaux}
    )
