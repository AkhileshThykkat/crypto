from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission: Only the owner of an object can edit/delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write/delete permissions only for the owner
        return obj.owner == request.user

class IsOrgOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission: Only the owner of the linked Organization can edit/delete CryptoPrices.
    """

    def has_object_permission(self, request, view, obj):
        # Allow read-only access (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if the user owns the Organization that the CryptoPrice belongs to
        return obj.org.owner == request.user