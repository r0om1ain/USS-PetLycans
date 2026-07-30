from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from space_agency.models import Vaisseau, Mission, Lieu
from space_agency.trajets import optimiser_trajet


class RouteTemplateTests(TestCase):
    def setUp(self):
        self.vaisseau = Vaisseau.objects.create(
            nom="USS Voyager", type=Vaisseau.TYPE_EXPLORATION, capacite=100
        )
        self.lieu = Lieu.objects.create(nom="Alpha Centauri")
        self.mission = Mission.objects.create(
            destination=self.lieu,
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

    def test_carte_trajet_page(self):
        response = self.client.get(f"/vaisseaux/{self.vaisseau.id}/carte/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "space_agency/carte_trajet.html")
        self.assertContains(response, "USS Voyager")
        self.assertContains(response, "Alpha Centauri")


class LieuDistanceTests(TestCase):
    def setUp(self):
        self.vaisseau = Vaisseau.objects.create(
            nom="NCC-1701", type=Vaisseau.TYPE_EXPLORATION, capacite=50
        )
        self.lieu_a = Lieu.objects.create(nom="Terre", x=0.0, y=0.0)
        self.lieu_b = Lieu.objects.create(nom="Mars", x=3.0, y=4.0)
        self.lieu_c = Lieu.objects.create(nom="Jupiter", x=10.0, y=0.0)

        self.mission_a = Mission.objects.create(
            destination=self.lieu_a,
            date_lancement=timezone.now().date(),
            statut=Mission.STATUT_PROGRAMMEE,
            vaisseau=self.vaisseau,
        )
        self.mission_b = Mission.objects.create(
            destination=self.lieu_b,
            date_lancement=timezone.now().date(),
            statut=Mission.STATUT_PROGRAMMEE,
            vaisseau=self.vaisseau,
        )
        self.mission_c = Mission.objects.create(
            destination=self.lieu_c,
            date_lancement=timezone.now().date(),
            statut=Mission.STATUT_PROGRAMMEE,
            vaisseau=self.vaisseau,
        )
        self.client = APIClient()

    def test_coords_auto_depuis_nom(self):
        lieu = Lieu.objects.create(nom="Nebuleuse-X")
        self.assertIsNotNone(lieu.x)
        self.assertIsNotNone(lieu.y)

        x, y = lieu.coords_depuis_nom()
        self.assertEqual(lieu.x, x)
        self.assertEqual(lieu.y, y)

    def test_distance_vers(self):
        self.assertAlmostEqual(self.lieu_a.distance_vers(self.lieu_b), 5.0)

    def test_optimiser_trajet(self):
        resultat = optimiser_trajet(
            [self.mission_a, self.mission_c, self.mission_b]
        )
        ids = []
        for mission in resultat["ordre"]:
            ids.append(mission.id)

        self.assertEqual(
            ids,
            [self.mission_a.id, self.mission_b.id, self.mission_c.id],
        )

    def test_api_distance(self):
        url = f"/api/missions/{self.mission_a.id}/distance/?vers={self.mission_b.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertAlmostEqual(response.data["distance"], 5.0)
        self.assertEqual(response.data["de"], "Terre")
        self.assertEqual(response.data["vers"], "Mars")

    def test_api_optimiser_trajet_vaisseau(self):
        url = f"/api/vaisseaux/{self.vaisseau.id}/optimiser-trajet/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["vaisseau"], "NCC-1701")
        self.assertEqual(len(response.data["ordre"]), 3)
        self.assertIn("distance_totale", response.data)
        self.assertEqual(len(response.data["etapes"]), 2)

    def test_api_optimiser_trajets_tous(self):
        response = self.client.get("/api/vaisseaux/optimiser-trajets/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["vaisseau_id"], self.vaisseau.id)

    def test_api_lieux_liste(self):
        response = self.client.get("/api/lieux/")
        self.assertEqual(response.status_code, 200)
