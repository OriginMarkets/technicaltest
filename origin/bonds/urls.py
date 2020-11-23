from django.urls import path
from bonds.views import BondViewSet

urlpatterns = [
    path('', BondViewSet.BondViewList.as_view(), name='bonds-lp'),
    path('<str:isin>', BondViewSet.BondViewDetail.as_view(), name='bonds-gud')
]