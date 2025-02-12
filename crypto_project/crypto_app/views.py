from rest_framework import generics, permissions,serializers
from rest_framework.response import Response
from .models import Organisation, CryptoPrice
from .serializers import OrganizationSerializer, CryptoPriceSerializer
from .permissions import IsOwnerOrReadOnly,IsOrgOwnerOrReadOnly

class OrganizationListCreate(generics.ListCreateAPIView):
    # queryset = Organisation.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Users should only see their own organizations"""
        return Organisation.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """Ensure the organization is created with the logged-in user as owner"""
        serializer.save(owner=self.request.user)

class OrganizationRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    # queryset = Organisation.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated,IsOwnerOrReadOnly]

    def get_queryset(self):
        """Users should only edit or delete their own organizations"""
        return Organisation.objects.filter(owner=self.request.user)

class CryptoPriceListCreate(generics.ListCreateAPIView):
    # queryset = CryptoPrice.objects.all()
    serializer_class = CryptoPriceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Users should only see crypto prices linked to their organization"""
        return CryptoPrice.objects.filter(org__owner=self.request.user)
    def perform_create(self, serializer):
        """Ensure users can only create Crypto Prices for their own organization"""
        user_organization = Organisation.objects.filter(owner=self.request.user).first()
        if user_organization:
            serializer.save(org=user_organization)
        else:
            raise serializers.ValidationError("You must have an organization to add crypto prices.")

class CryptoPriceRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    # queryset = CryptoPrice.objects.all()
    serializer_class = CryptoPriceSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrgOwnerOrReadOnly]

    def get_queryset(self):
        """Users can only see and modify crypto prices linked to their organization."""
        return CryptoPrice.objects.filter(org__owner=self.request.user)
