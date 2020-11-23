from django.urls import path
from bonds.views import HelloWorld
from rest_framework.authtoken import views
from django.contrib.auth import login
from bonds import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HelloWorld.as_view()),
    #path('bonds/', BondsListAPIView.as_view()),
    path('api-token-auth/', views.obtain_auth_token),
    path('bonds/', views.bonds_data),
]