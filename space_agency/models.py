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


class Lieu(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    x = models.FloatField(blank=True, null=True)
    y = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = "Lieu"
        verbose_name_plural = "Lieux"

    def coords_depuis_nom(self):
        """Inventer des coordonnées fictives à partir du nom du lieu."""
        total = 0
        for lettre in self.nom:
            total = total + ord(lettre)

        x = (total % 2000) - 1000
        y = ((total * 7) % 2000) - 1000
        return x, y

    def save(self, *args, **kwargs):
        # Si aucune coordonnée n'est fournie, on les crée à partir du nom
        if self.x is None and self.y is None:
            self.x, self.y = self.coords_depuis_nom()
        super().save(*args, **kwargs)

    def distance_vers(self, autre):
        """Distance euclidienne 2D entre ce lieu et un autre."""
        dx = self.x - autre.x
        dy = self.y - autre.y
        return (dx * dx + dy * dy) ** 0.5

    def __str__(self):
        return self.nom


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

    destination = models.ForeignKey(
        Lieu, on_delete=models.PROTECT, related_name="missions"
    )
    date_lancement = models.DateField()
    statut = models.CharField(
        max_length=50, choices=STATUT_CHOICES, default=STATUT_PROGRAMMEE
    )
    vaisseau = models.ForeignKey(
        Vaisseau, on_delete=models.CASCADE, related_name="missions"
    )

    def __str__(self):
        return f"Mission {self.destination} ({self.statut})"
