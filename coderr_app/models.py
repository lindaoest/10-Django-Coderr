from django.db import models
from auth_app.models import CustomerProfile, BusinessProfile

STATUS_CHOICES = [
    ('in_progress', 'In Bearbeitung'),
    ('completed', 'Abgeschlossen'),
    ('cancelled', 'Abgebrochen'),
]

TYPECHOICES = [
	("base", "Base"),
	("standard", "Standard"),
	("premium", "Premium")
]

class Offer(models.Model):
	title = models.CharField(max_length=366)
	text = models.TextField(blank=True)
	createdAt = models.DateTimeField(auto_now_add=True)
	image = models.FileField(upload_to='single_offer/')
	business_user = models.ForeignKey(BusinessProfile, related_name='offer', on_delete=models.CASCADE)

class OfferOption(models.Model):
	title = models.CharField(max_length=366)
	price = models.FloatField()
	offer_type = models.CharField(choices=TYPECHOICES, default='base')
	delivery_time_in_days = models.CharField()
	revisions = models.CharField(max_length=155)
	list = models.TextField()
	features = models.JSONField()
	offer = models.ForeignKey(Offer, related_name='offerOption', on_delete=models.CASCADE)

class Order(models.Model):
	status = models.CharField(choices=STATUS_CHOICES, default='in_progress')
	createdAt = models.DateTimeField(auto_now_add=True)
	offer_detail_id = models.ForeignKey(Offer, related_name='orders', on_delete=models.CASCADE)
	customer_user = models.ForeignKey(CustomerProfile, related_name='orders', on_delete=models.CASCADE)
	business_user = models.ForeignKey(BusinessProfile, related_name='orders', on_delete=models.CASCADE)


class Review(models.Model):
	description = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	rating = models.IntegerField()
	offer = models.ForeignKey(Offer, related_name='reviews', on_delete=models.CASCADE)
	reviewer = models.ForeignKey(CustomerProfile, related_name='reviews', on_delete=models.CASCADE)
	business_user = models.ForeignKey(BusinessProfile, related_name='reviews', on_delete=models.CASCADE)



