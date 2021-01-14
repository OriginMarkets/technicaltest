
from rest_framework import generics, permissions
from rest_framework.viewsets import ModelViewSet

from .models import Bond
from .serializers import BondSerializer  # , UserSerializer



from rest_framework.views import APIView
from rest_framework.response import Response


class HelloWorld(APIView):
    def get(self, request):
        return Response("Hello World!")


class BondViewSet(ModelViewSet):
    serializer_class = BondSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        
        return Bond.objects.filter(owner=self.request.user) 
    
    def filter_queryset(self, queryset):
        
        if 'legal_name' in self.request.GET:
            return queryset.filter(legal_name=self.request.GET['legal_name'])
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)

    

