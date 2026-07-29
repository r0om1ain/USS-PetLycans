from django.db import models


class Vaisseau(models.Model):
    TYPE_EXPLORATION = "Exploration"
    TYPE_CARGO = "Cargo"
    TYPE_TRANSPORT = "Transport"
    TYPE_COMBAT = "Combat"

    TYPE_CHOICES = [
        (TYPE_EXPLORATION, "Exploration"),
        (TYPE_CARGO, "Cargo"),
        (TYPE_TRANSPORT, "Transport"),
        (TYPE_COMBAT, "Combat"),
    ]

    nom = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    capacite = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.nom} ({self.type})"

    class Meta:
        verbose_name = "Vaisseau"
        verbose_name_plural = "Vaisseaux"



class Mission(models.Model):
    STATUT_PROGRAMMEE = "Programmée"
    STATUT_EN_COURS = "En cours"
    STATUT_TERMINEE = "Terminée"
    STATUT_ANNULEE = "Annulée"

    STATUT_CHOICES = [
        (STATUT_PROGRAMMEE, "Programmée"),
        (STATUT_EN_COURS, "En cours"),
        (STATUT_TERMINEE, "Terminée"),
        (STATUT_ANNULEE, "Annulée"),
    ]

    destination = models.CharField(max_length=100)
    date_lancement = models.DateField()
    statut = models.CharField(
        max_length=50, choices=STATUT_CHOICES, default=STATUT_PROGRAMMEE
    )
    vaisseau = models.ForeignKey(
        Vaisseau, on_delete=models.CASCADE, related_name="missions"
    )

    def __str__(self):
        return f"Mission {self.destination} ({self.statut})"
