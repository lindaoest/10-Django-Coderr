from django.db import models
from auth_app.models import CustomerProfile, BusinessProfile
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
	# min_price = models.DecimalField(max_digits=8, decimal_places=2)
	# min_delivery_time = models.IntegerField()

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
	# list = models.TextField()

class Order(models.Model):
	customer_user = models.ForeignKey(CustomerProfile, related_name='orders', on_delete=models.CASCADE)
	business_user = models.ForeignKey(BusinessProfile, related_name='orders', on_delete=models.CASCADE)
	title = models.CharField(max_length=255)
	revisions = models.IntegerField()
	delivery_time_in_days = models.IntegerField()
	price = models.DecimalField(max_digits=8, decimal_places=2)
	features = models.JSONField()
	offer_type = models.CharField(choices=TYPECHOICES, default='basic')
	status = models.CharField(choices=STATUS_CHOICES, default='in_progress')
	# list = models.TextField()
	# offer = models.ForeignKey(Offer, related_name='offerOption', on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	# offer_detail_id = models.ForeignKey(Offer, related_name='orders', on_delete=models.CASCADE)

	def __str__(self):
		return {self.title}

class CompletedOrderCount(models.Model):
	completed_order_count = models.IntegerField()

class Review(models.Model):
	business_user = models.ForeignKey(BusinessProfile, related_name='reviews', on_delete=models.CASCADE)
	reviewer = models.ForeignKey(CustomerProfile, related_name='reviews', on_delete=models.CASCADE)
	rating = models.DecimalField(max_digits=8, decimal_places=2)
	description = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	# offer = models.ForeignKey(Offer, related_name='reviews', on_delete=models.CASCADE)

class BaseInfo(models.Model):
	review_count = models.IntegerField()
	average_rating = models.DecimalField(max_digits=3, decimal_places=2)
	business_profile_count = models.IntegerField()
	offer_count = models.IntegerField()

