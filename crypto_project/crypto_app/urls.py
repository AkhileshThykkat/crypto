from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import OrganizationListCreate, OrganizationRetrieveUpdateDestroy, CryptoPriceListCreate, CryptoPriceRetrieveUpdateDestroy

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('organizations/', OrganizationListCreate.as_view(), name='organization-list'),
    path('organizations/<uuid:pk>/', OrganizationRetrieveUpdateDestroy.as_view(), name='organization-detail'),
    path('crypto-prices/', CryptoPriceListCreate.as_view(), name='crypto-price-list'),
    path('crypto-prices/<int:pk>/', CryptoPriceRetrieveUpdateDestroy.as_view(), name='crypto-price-detail'),
]

# urlpatterns += [
#     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
# ]
