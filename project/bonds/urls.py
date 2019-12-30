from django.urls import path

from project.bonds.views import BondListView


app_name = "bonds"
urlpatterns = [
    path("", BondListView.as_view(), name="list-view"),
]
