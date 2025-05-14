from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS

class OfferPermission(BasePermission):
	def has_permission(self, request, view):
		if request.method in SAFE_METHODS:
			return True
		elif request.method == 'POST' and hasattr(request.user, 'businessProfile'):
			return True

		return hasattr(request.user, 'businessProfile')

	def has_object_permission(self, request, view, obj):
		if request.method in SAFE_METHODS:
			return True
		elif request.method in ['PATCH', 'PUT', 'DELETE'] and request.user == obj.user:
			return True
		else:
			return False

class OrderPermission(BasePermission):
	def has_permission(self, request, view):
		if request.method in SAFE_METHODS and request.user.is_authenticated:
			return True
		elif request.method == 'POST' and request.user.is_authenticated and hasattr(request.user, 'customerProfile'):
			return True

		return request.user.is_authenticated

	def has_object_permission(self, request, view, obj):
		if request.method in SAFE_METHODS:
			return True
		elif request.method in ['PATCH', 'PUT'] and request.user == obj.business_user:
			return True
		elif request.method == 'DELETE' and request.user.is_stuff:
			return True
		else:
			return False

class ReviewPermission(BasePermission):
	def has_permission(self, request, view):
		if request.method in SAFE_METHODS and request.user.is_authenticated:
			return True
		elif request.method == 'POST' and request.user.is_authenticated and hasattr(request.user, 'customerProfile'):
			return True

		return request.user.is_authenticated

	def has_object_permission(self, request, view, obj):
		if request.method in SAFE_METHODS:
			return True
		elif request.method in ['PATCH', 'DELETE'] and request.user == obj.reviewer:
			return True
		else:
			return False