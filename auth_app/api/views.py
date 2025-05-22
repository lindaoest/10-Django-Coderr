from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .serializers import RegistrationSerializer, BusinessProfileSerializer, CustomerProfileSerializer
from ..models import BusinessProfile, CustomerProfile
from .permissions import ProfilePermission

""" View for user registration - anyone can access """
class RegistrationView(APIView):
	permission_classes = [AllowAny]

	def post(self, request, *args, **kwargs):
		serializer = RegistrationSerializer(data=request.data)

		# Check if input data is valid
		if serializer.is_valid():
			# Save user and create a token
			user = serializer.save()
			token, created = Token.objects.get_or_create(user=user)

			# Return token and user info in response
			return Response({
				'token': token.key,
				'user_id': user.pk,
				'email': user.email,
				'username': user.username
			}, status=status.HTTP_201_CREATED)

		# Return validation errors if input is invalid
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

""" View for user login - inherits default ObtainAuthToken behavior """
class LoginView(ObtainAuthToken):
	permission_classes = [AllowAny]

	def post(self, request, *args, **kwargs):
		serializer = self.serializer_class(data=request.data)

		# Validate credentials
		if serializer.is_valid():
			user = serializer.validated_data['user']
			# Get or create authentication token for user
			token, created = Token.objects.get_or_create(user=user)

			# Return token and user info
			return Response({
				'token': token.key,
				'user_id': user.pk,
				'email': user.email,
				'username': user.username
			}, status=status.HTTP_201_CREATED)

		# Return errors if authentication fails
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

""" View to retrieve or partially update user profiles (Business or Customer) """
class ProfileDetailView(APIView):
	permission_classes = [ProfilePermission]

	def get(self, request, pk):
		user = get_object_or_404(User, pk=pk)

		# Check if user has a CustomerProfile and serialize it
		if hasattr(user, 'customerProfile'):
			userCustomer = CustomerProfile.objects.get(user_id=pk)
			serializer = CustomerProfileSerializer(userCustomer)
		# Else check if user has a BusinessProfile and serialize it
		elif hasattr(user, 'businessProfile'):
			userBusiness = BusinessProfile.objects.get(user_id=pk)
			serializer = BusinessProfileSerializer(userBusiness)

		# Return serialized profile data
		return Response(serializer.data)

	# Handle individual PATCH request
	def patch(self, request, pk):
		user = get_object_or_404(User, pk=pk)

		# Partial update: select serializer based on profile type
		if hasattr(user, 'customerProfile'):
			userCustomer = CustomerProfile.objects.get(user_id=pk)
			# Check object-level permission
			self.check_object_permissions(request, userCustomer)
			serializer = CustomerProfileSerializer(userCustomer, data=request.data, partial=True)
		else:
			userBusiness = BusinessProfile.objects.get(user_id=pk)
			# Check object-level permission
			self.check_object_permissions(request, userBusiness)
			serializer = BusinessProfileSerializer(userBusiness, data=request.data, partial=True)

		# Validate and save changes
		if serializer.is_valid():
			user = serializer.save()
			return Response(serializer.data)

		# Return validation errors if update invalid
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

""" List and create view for all BusinessProfiles """
class ProfileBusinessView(generics.ListCreateAPIView):
	queryset = BusinessProfile.objects.all()
	serializer_class = BusinessProfileSerializer

""" List and create view for all CustomerProfiles """
class ProfileCustomerView(generics.ListCreateAPIView):
	queryset = CustomerProfile.objects.all()
	serializer_class = CustomerProfileSerializer