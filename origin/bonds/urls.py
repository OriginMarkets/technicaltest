from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from .views import BondViewSet

router = DefaultRouter()
router.register("bonds", BondViewSet, 'bonds')

urlpatterns = router.urls


