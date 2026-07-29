from django.test import TestCase
from django.urls import reverse
from space_agency.models import Vaisseau, Mission
from django.utils import timezone


class RouteTemplateTests(TestCase):
    def setUp(self):
        self.vaisseau = Vaisseau.objects.create(
            nom="USS Voyager", type=Vaisseau.TYPE_EXPLORATION, capacite=100
        )
        self.mission = Mission.objects.create(
            destination="Alpha Centauri",
            date_lancement=timezone.now().date(),
            statut=Mission.STATUT_PROGRAMMEE,
            vaisseau=self.vaisseau,
        )

    def test_route_missions_renders_tableau_missions(self):
        response = self.client.get("/missions/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "space_agency/tableau_missions.html")
        self.assertContains(response, "Alpha Centauri")

    def test_route_vaisseaux_renders_tableau_vaisseaux(self):
        response = self.client.get("/vaisseaux/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "space_agency/tableau_vaisseaux.html")
        self.assertContains(response, "USS Voyager")
