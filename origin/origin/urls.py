
from django.contrib import admin
from django.urls import path

from bonds.views import HelloWorld

from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HelloWorld.as_view()),
    path('', include('bonds.urls')),
]


urlpatterns += [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
]
