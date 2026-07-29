from django.contrib import admin
from .models import Vaisseau, Mission

admin.site.register(Vaisseau)

@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ("destination", "date_lancement", "statut", "vaisseau")
    list_filter = ("statut", "date_lancement")
    search_fields = ("destination", "vaisseau__nom")

