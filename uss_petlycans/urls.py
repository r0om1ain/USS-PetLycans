from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from space_agency import views

urlpatterns = [
    path("", views.home, name="home"),
    path("admin/", admin.site.urls),
    path("missions/", views.tableau_missions, name="tableau_missions"),
    path("vaisseaux/", views.tableau_vaisseaux, name="tableau_vaisseaux"),
    path("vaisseaux/<int:pk>/carte/", views.carte_trajet, name="carte_trajet"),
    path("api/", include("space_agency.api_urls"), name="api"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
