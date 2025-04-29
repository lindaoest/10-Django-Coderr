from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import RegistrationSerializer

class RegistrationView(APIView):
	permission_classes = [AllowAny]

	def post(self, request, *args, **kwargs):

		serializer = RegistrationSerializer(data=request.data)

		if serializer.is_valid():
			user = serializer.save()
			token, created = Token.objects.get_or_create(user=user)

			return Response({
				'token': token.key,
				'user_id': user.pk,
				'email': user.email,
				'username': user.username
			})

class LoginView(generics.ListCreateAPIView):
	pass

class ProfileView(generics.ListCreateAPIView):
	pass

class ProfileBusinessView(generics.ListCreateAPIView):
	pass

class ProfileCustomerView(generics.ListCreateAPIView):
	pass