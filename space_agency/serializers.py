from datetime import datetime
from rest_framework import serializers
from .models import Vaisseau, Mission, Lieu


class VaisseauSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaisseau
        fields = ["id", "nom", "type", "capacite"]


class LieuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lieu
        fields = ["id", "nom", "x", "y"]


class MissionSerializer(serializers.ModelSerializer):
    destination_nom = serializers.CharField(source="destination.nom", read_only=True)

    class Meta:
        model = Mission
        fields = [
            "id",
            "destination",
            "destination_nom",
            "date_lancement",
            "statut",
            "vaisseau",
        ]

    def validate(self, data):
        statut = data.get("statut")
        date_lancement = data.get("date_lancement")

        if statut == Mission.STATUT_PROGRAMMEE and date_lancement is not None:
            if date_lancement < datetime.now().date():
                raise serializers.ValidationError(
                    "Une mission programmée ne peut pas avoir une date dans le passé"
                )
        return data
