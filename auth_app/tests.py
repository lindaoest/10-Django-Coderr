from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from auth_app.models import CustomerProfile
from .api.serializers import CustomerProfileSerializer

class RegistrationTests(APITestCase):
	def test_create_registration(self):
		url = reverse('registration-list')
		data = {
			"username": "Martha123",
			"email": "martha@mail.de",
			"password": "123456789",
			"repeated_password": "123456789",
			"type": "customer"
		}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class LoginTests(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='Martha123', email='martha@gmail.com', password='123456789')
		CustomerProfile.objects.create(
			user=self.user,
			email='martha@gmail.com',
			type='customer',
			username='Martha123'
		)

		# Authentication with token
		self.token = Token.objects.create(user=self.user)
		self.client = APIClient()
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

	def test_create_login(self):
		url = reverse('login-list')
		data = {
			"username": "Martha123",
			"password": "123456789"
		}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class ProfileTests(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='Martha123', email='martha@gmail.com', password='123456789')
		self.customer = CustomerProfile.objects.create(
			user=self.user,
			email='martha@gmail.com',
			type='customer',
			username='Martha123',
			first_name= 'Martha',
			last_name='Egger',
			file= None
		)

		# Authentication with token
		self.token = Token.objects.create(user=self.user)
		self.client = APIClient()
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

	def test_detail_profile(self):
		url = reverse('profile-detail', kwargs={'pk': self.customer.id})
		response = self.client.get(url)

		expected_data = CustomerProfileSerializer(self.customer).data

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data, expected_data)

	def test_detail_patch__profile(self):
		url = reverse('profile-detail', kwargs={'pk': self.customer.id})

		data = {
			"first_name": "Martha",
			"last_name": "Egger",
			"location": "Bozen",
			"tel": "335865147",
			"description": "",
			"working_hours": "10-18",
			"email": "martha@gmail.com"
		}
		response = self.client.patch(url, data, format='json')
		expected_data = CustomerProfileSerializer(self.customer).data

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data, expected_data)