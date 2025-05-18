from rest_framework.permissions import BasePermission, SAFE_METHODS

# Custom permission to check profile ownership and authentication
class ProfilePermission(BasePermission):
	# Check if the user is authenticated for general access
	def has_permission(self, request, view):
		return request.user and request.user.is_authenticated

	# Check object-level permissions:
    # Allow safe methods (GET, HEAD, OPTIONS) for who is authenticated
    # Only allow actions if the requesting user owns the object
	def has_object_permission(self, request, view, obj):
		if request.method in SAFE_METHODS and request.user.is_authenticated:
			return True

		return request.user == obj.user