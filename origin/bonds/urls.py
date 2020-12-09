from django.urls import include, path
from .views import BondViewSet

urlpatterns = [
    path("", BondViewSet.as_view(
        {'get': 'list', "post": "create"}
    ))
]
