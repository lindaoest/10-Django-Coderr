from django.db import models
from django.contrib.auth.models import User

STATUS_CHOICES = [
    ('in_progress', 'In Bearbeitung'),
    ('completed', 'Abgeschlossen'),
    ('cancelled', 'Abgebrochen'),
]

TYPECHOICES = [
	("basic", "Basic"),
	("standard", "Standard"),
	("premium", "Premium")
]

class Offer(models.Model):
	user = models.ForeignKey(User, related_name='offers', on_delete=models.CASCADE)
	title = models.CharField(max_length=255)
	image = models.FileField(upload_to='offers/', null=True)
	description = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	min_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
	min_delivery_time = models.IntegerField(default=5)

	def __str__(self):
		return f"{self.title} (ID: {self.id})"

class OfferDetail(models.Model):
	title = models.CharField(max_length=255)
	revisions = models.IntegerField()
	delivery_time_in_days = models.IntegerField()
	price = models.DecimalField(max_digits=8, decimal_places=2)
	features = models.JSONField()
	offer_type = models.CharField(choices=TYPECHOICES, default='basic')
	offer = models.ForeignKey(Offer, related_name='details', on_delete=models.CASCADE)

class Order(models.Model):
	customer_user = models.ForeignKey(User, related_name='orders_customer_user', on_delete=models.CASCADE)
	business_user = models.ForeignKey(User, related_name='orders_business_user', on_delete=models.CASCADE)
	title = models.CharField(max_length=255)
	revisions = models.IntegerField()
	delivery_time_in_days = models.IntegerField()
	price = models.DecimalField(max_digits=8, decimal_places=2)
	features = models.JSONField()
	offer_type = models.CharField(choices=TYPECHOICES, default='basic')
	status = models.CharField(choices=STATUS_CHOICES, default='in_progress')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return {self.title}

class Review(models.Model):
	business_user = models.ForeignKey(User, related_name='reviews_business_user', on_delete=models.CASCADE)
	reviewer = models.ForeignKey(User, related_name='reviews_reviewer', on_delete=models.CASCADE)
	rating = models.DecimalField(max_digits=8, decimal_places=2)
	description = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)