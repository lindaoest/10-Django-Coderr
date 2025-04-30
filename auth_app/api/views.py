from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import RegistrationSerializer, ProfileSerializer
from rest_framework import status
from ..models import UserProf
from django.contrib.auth.models import User

class RegistrationView(APIView):
	permission_classes = [AllowAny]

	def post(self, request, *args, **kwargs):

		serializer = RegistrationSerializer(data=request.data)

		if serializer.is_valid():
			user = serializer.save()
			token, created = Token.objects.get_or_create(user=user.user)

			return Response({
				'token': token.key,
				'user_id': user.user.pk,
				'email': user.user.email,
				'username': user.user.username
			})
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.ListCreateAPIView):
	pass

class ProfileView(generics.RetrieveUpdateDestroyAPIView):
	queryset = User.objects.all()
	serializer_class = ProfileSerializer
	permission_classes = [AllowAny]

class ProfileBusinessView(generics.ListCreateAPIView):
	pass

class ProfileCustomerView(generics.ListCreateAPIView):
	pass