from django.contrib import admin
from .models import Vaisseau, Mission, Lieu


@admin.register(Vaisseau)
class VaisseauAdmin(admin.ModelAdmin):
    list_display = ("nom", "type", "capacite")
    search_fields = ("nom",)


@admin.register(Lieu)
class LieuAdmin(admin.ModelAdmin):
    list_display = ("nom", "x", "y")
    search_fields = ("nom",)


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ("destination", "date_lancement", "statut", "vaisseau")
    list_filter = ("statut", "date_lancement")
    search_fields = ("destination__nom", "vaisseau__nom")
