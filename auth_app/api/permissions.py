from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView

class ProfilePermission(BasePermission):
	def has_permission(self, request, view):
		return request.user and request.user.is_authenticated

	def has_object_permission(self, request, view, obj):
		if request.method in SAFE_METHODS:
			return True

		return request.user == obj.user