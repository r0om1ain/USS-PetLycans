from datetime import datetime
from rest_framework import serializers
from .models import Vaisseau, Mission



class VaisseauSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vaisseau
        fields = ['id', 'nom', 'type', 'capacite']



class MissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = ['id', 'destination', 'date_lancement', 'statut', 'vaisseau']


    def validate(self, data):
        statut = data.get('statut')
        date_lancement = data.get('date_lancement')
        if statut == "Programmée" and date_lancement < datetime.now().date():
            raise serializers.ValidationError(
                "Une mission programmée ne peut pas avoir une date de lancement dans le passé"
            )
        return data


