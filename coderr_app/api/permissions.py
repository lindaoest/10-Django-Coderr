from rest_framework.permissions import BasePermission, SAFE_METHODS

class OfferPermission(BasePermission):
    def has_permission(self, request, view):
        # Safe methods require authenticated user
        if request.method in SAFE_METHODS:
            return True

        # For POST, user must be authenticated and have a business profile
        if request.method == 'POST':
            return request.user.is_authenticated and hasattr(request.user, 'businessProfile')

        # For other methods, user must be authenticated and have business profile
        return request.user.is_authenticated and hasattr(request.user, 'businessProfile')

    def has_object_permission(self, request, view, obj):
        # Safe methods require authentication
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated

        # Update and delete allowed only if user owns the object
        if request.method in ['PATCH', 'PUT', 'DELETE']:
            return request.user.is_authenticated and request.user == obj.user

        return False

class OrderPermission(BasePermission):
    def has_permission(self, request, view):
        # Safe methods require authenticated user
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated

        # POST requires authenticated user with customer profile
        if request.method == 'POST':
            return request.user.is_authenticated and hasattr(request.user, 'customerProfile')

        # Other methods require authentication
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Safe methods require authenticated user
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated

        # Update (PATCH, PUT) allowed only if user is business user of the order
        if request.method in ['PATCH', 'PUT']:
            return request.user.is_authenticated and request.user == obj.business_user

        # Delete allowed only if user is staff
        if request.method == 'DELETE':
            return request.user.is_staff

        return False

class ReviewPermission(BasePermission):
    def has_permission(self, request, view):
        # Safe methods require authenticated user
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated

        # POST requires authenticated user with customer profile
        if request.method == 'POST':
            return request.user.is_authenticated and hasattr(request.user, 'customerProfile')

        # Other methods require authentication
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Update and delete allowed only if user is the reviewer
        if request.method in ['PATCH', 'DELETE']:
            return request.user.is_authenticated and request.user == obj.reviewer

        return False