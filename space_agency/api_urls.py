from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("vaisseaux", views.VaisseauViewSet)
router.register("missions", views.MissionViewSet)
router.register("lieux", views.LieuViewSet)

urlpatterns = router.urls
