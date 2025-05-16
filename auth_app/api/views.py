from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import RegistrationSerializer, BusinessProfileSerializer, CustomerProfileSerializer
from rest_framework import status
from ..models import BusinessProfile, CustomerProfile
from rest_framework.authtoken.views import ObtainAuthToken
from .permissions import ProfilePermission
from django.contrib.auth.models import User

class RegistrationView(APIView):
	permission_classes = [AllowAny]

	def post(self, request, *args, **kwargs):
		serializer = RegistrationSerializer(data=request.data)

		# If the serializer is valid, generate a token and return a response with token, user ID, email, and username
		if serializer.is_valid():
			user = serializer.save()
			token, created = Token.objects.get_or_create(user=user)

			return Response({
				'token': token.key,
				'user_id': user.pk,
				'email': user.email,
				'username': user.username
			})
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(ObtainAuthToken):
	permission_classes = [AllowAny]

	def post(self, request, *args, **kwargs):
		serializer = self.serializer_class(data=request.data)

		# If the serializer is valid, get the token for the user who is logged in and return a response
		# with token, user ID, email, and username
		if serializer.is_valid():
			user = serializer.validated_data['user']
			token, created = Token.objects.get_or_create(user=user)

			return Response({
				'token': token.key,
				'user_id': user.pk,
				'email': user.email,
				'username': user.username
			})

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileDetailView(APIView):
	permission_classes = [ProfilePermission]

	def get(self, request, pk):
		user = User.objects.get(pk=pk)

		# Show BusinessProfile or CustomerProfile based on type and ID from URL
		if hasattr(user, 'customerProfile'):
			userCustomer = CustomerProfile.objects.get(user_id=pk)
			serializer = CustomerProfileSerializer(userCustomer)
		elif hasattr(user, 'businessProfile'):
			userBusiness = BusinessProfile.objects.get(user_id=pk)
			serializer = BusinessProfileSerializer(userBusiness)

		return Response(serializer.data)

	# Handle individual PATCH request
	def patch(self, request, pk):
		user = User.objects.get(pk=pk)

		if hasattr(user, 'customerProfile'):
			userCustomer = CustomerProfile.objects.get(user_id=pk)
			serializer = CustomerProfileSerializer(userCustomer, data=request.data, partial=True)
		else:
			userBusiness = BusinessProfile.objects.get(user_id=pk)
			serializer = BusinessProfileSerializer(userBusiness, data=request.data, partial=True)

		if serializer.is_valid():
			user = serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileBusinessView(generics.ListCreateAPIView):
	queryset = BusinessProfile.objects.all()
	serializer_class = BusinessProfileSerializer

class ProfileCustomerView(generics.ListCreateAPIView):
	queryset = CustomerProfile.objects.all()
	serializer_class = CustomerProfileSerializer