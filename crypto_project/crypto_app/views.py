from rest_framework import generics, permissions,serializers,filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Organisation, CryptoPrice
from .serializers import OrganizationSerializer, CryptoPriceSerializer
from .permissions import IsOwnerOrReadOnly,IsOrgOwnerOrReadOnly

class OrganizationListCreate(generics.ListCreateAPIView):
    # queryset = Organisation.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name'] 
    ordering_fields = ['created_at'] 


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
    pagination_class = PageNumberPagination

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
    def perform_update(self, serializer):
        """Ensure the correct org is used based on the logged-in user."""
        crypto_price = self.get_object()

        if crypto_price.org.owner != self.request.user:
            raise PermissionDenied("You do not have permission to update this price.")
        serializer.save(org=crypto_price.org)
    
    def perform_destroy(self, instance):
        """Ensure only the org owner can delete the price."""
        if instance.org.owner != self.request.user:
            raise PermissionDenied("You do not have permission to delete this price.")

        instance.delete()
