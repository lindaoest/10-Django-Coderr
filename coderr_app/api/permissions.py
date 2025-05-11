from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView

class ReviewPermission(BasePermission):
	def has_permission(self, request, view):
		if request.method == 'GET' and request.user.is_authenticated:
			return True
		elif request.method == 'POST' and request.user.is_authenticated and hasattr(request.user, 'customerProfile'):
			return True
		else:
			return False

	def has_object_permission(self, request, view, obj):
		if request.method == 'GET' and request.user.is_authenticated:
			return True
		elif request.method in ['PATCH', 'DELETE'] and request.user == obj.reviewer:
			return True
		else:
			return False

class OrderPermission(BasePermission):
	def has_permission(self, request, view):
		if request.method == 'GET' and request.user.is_authenticated:
			return True
		elif request.method == 'POST' and request.user.is_authenticated and hasattr(request.user, 'customerProfile'):
			return True
		else:
			return False

	def has_object_permission(self, request, view, obj):
		if request.method == 'GET' and request.user.is_authenticated:
			return True
		elif request.method in ['PATCH', 'DELETE'] and request.user == obj.reviewer:
			return True
		else:
			return False