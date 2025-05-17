from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import Offer, OfferDetail
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from auth_app.models import BusinessProfile, CustomerProfile

class OfferTests(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='Karin', email='karin@gmail.com', password='123456789')
		BusinessProfile.objects.create(
			user=self.user,
			email='karin@gmail.com',
			type='business',
			username='Karin'
		)

		# Authentication with token
		self.token = Token.objects.create(user=self.user)
		self.client = APIClient()
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

	def test_get_offer(self):
		url = reverse('offer-list')
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_create_offer(self):
		url = reverse('offer-list')
		data = {
			"title": "Angular Frontend Entwicklungspaket",
			"image": None,
			"description": "Ein umfassendes Dienstleistungspaket für die Entwicklung moderner, responsiver Angular-Frontends – ideal für Start-ups, Agenturen und Unternehmen.",
			"details": [
				{
				"title": "Basic Angular Setup",
				"revisions": 1,
				"delivery_time_in_days": 3,
				"price": 300,
				"features": [
					"Initiales Angular-Projektsetup",
					"1 statische Seite mit responsivem Layout",
					"Integration von Angular Material",
					"Deployment-Anleitung"
				],
				"offer_type": "basic"
				},
				{
				"title": "Standard Angular Web App",
				"revisions": 3,
				"delivery_time_in_days": 7,
				"price": 700,
				"features": [
					"Bis zu 3 dynamische Seiten (z. B. Landingpage, Dashboard, Kontaktformular)",
					"Responsive Design & State Management (z. B. mit NgRx oder Signals)",
					"REST-API-Anbindung",
					"Fehlermeldungs- & Ladezustands-Handling"
				],
				"offer_type": "standard"
				},
				{
				"title": "Premium Angular Enterprise Paket",
				"revisions": 5,
				"delivery_time_in_days": 14,
				"price": 1500,
				"features": [
					"Bis zu 7 Seiten mit komplexer Logik und Interaktionen",
					"Komponenten-Architektur mit Wiederverwendbarkeit",
					"Formularvalidierungen & Authentifizierung",
					"Testing (Unit- und E2E mit Jasmine/Karma oder Cypress)",
					"Performanceoptimierung & Lighthouse-Audit"
				],
				"offer_type": "premium"
				}
			]
		}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Offer.objects.count(), 1)
		self.assertEqual(Offer.objects.get().title, 'Angular Frontend Entwicklungspaket')

class OrderTests(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='Kira', email='kira@gmail.com', password='123456789')
		self.customer = CustomerProfile.objects.create(
			user=self.user,
			email='kira@gmail.com',
			type='customer',
			username='Kira'
		)
		self.business_user = BusinessProfile.objects.create(
			user=self.user,
			email='karin@gmail.com',
			type='business',
			username='Karin'
		)

		# Authentication with token
		self.token = Token.objects.create(user=self.user)
		self.client = APIClient()
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

	def test_get_order(self):
		url = reverse('order-list')
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_create_order(self):
		url = reverse('order-list')
		offer = Offer.objects.create(
			user = self.user,
			title = 'Angular Frontend Entwicklungspaket',
			image = None,
			description = 'Ein umfassendes Dienstleistungspaket für die Entwicklung moderner, responsiver Angular-Frontends – ideal für Start-ups, Agenturen und Unternehmen.',
			min_price = 300,
			min_delivery_time = 7
		)
		OfferDetail.objects.create(
			offer=offer,
			title = 'Basic Angular Setup',
			revisions = 1,
			delivery_time_in_days = 3,
			price = 300,
			features = [
				'Initiales Angular-Projektsetup',
				'1 statische Seite mit responsivem Layout',
				'Integration von Angular Material',
				'Deployment-Anleitung'
			],
			offer_type = 'basic'
		)
		OfferDetail.objects.create(
			offer=offer,
			title = 'Standard Angular Setup',
			revisions = 3,
			delivery_time_in_days = 6,
			price = 500,
			features = [
				'Initiales Angular-Projektsetup',
				'1 statische Seite mit responsivem Layout',
				'Integration von Angular Material',
				'Deployment-Anleitung'
			],
			offer_type = 'standard'
		)
		OfferDetail.objects.create(
			offer=offer,
			title = 'Premium Angular Setup',
			revisions = 6,
			delivery_time_in_days = 7,
			price = 1000,
			features = [
				'Initiales Angular-Projektsetup',
				'1 statische Seite mit responsivem Layout',
				'Integration von Angular Material',
				'Deployment-Anleitung'
			],
			offer_type = 'premium'
		)
		data = {
			"business_id": self.business_user.id,
			"delivery_time_in_days": 7,
			"features": ["Bis zu 3 Modelle mit Relationen", "JWT- oder OAuth2-Authentifizierung"],
			"offer_type": "standard",
			"price": 500,
			"revisions": 3,
			"status": "completed",
			"title": "Standard API",
			"offer_detail_id": offer.id
		}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class ReviewTests(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='Kira', email='kira@gmail.com', password='123456789')
		CustomerProfile.objects.create(
			user=self.user,
			email='kira@gmail.com',
			type='customer',
			username='Kira'
		)
		self.business_user = BusinessProfile.objects.create(
			user=self.user,
			email='karin@gmail.com',
			type='business',
			username='Karin'
		)

		# Authentication with token
		self.token = Token.objects.create(user=self.user)
		self.client = APIClient()
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

	def test_get_review(self):
		url = reverse('review-list')
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_create_review(self):
		url = reverse('review-list')
		data = {
			"business_user": self.business_user.id,
			"description": "Hervorragende Zusammenarbeit! Kann ich weiterempfehlen",
			"rating": "5.00"
		}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)