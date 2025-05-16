from django.db import models
from django.contrib.auth.models import User

TYPECHOICES = [
	("business", "Business"),
	("customer", "Customer")
]

class CustomerProfile(models.Model):
	user = models.OneToOneField(User, related_name="customerProfile", on_delete=models.CASCADE)
	type = models.CharField(max_length=50, choices=TYPECHOICES, default='customer')
	username = models.CharField(max_length=150, blank=True)
	first_name = models.CharField(max_length=30, blank=True)
	last_name = models.CharField(max_length=30, blank=True)
	file = models.FileField(upload_to='profile_pictures/', null=True, blank=True)
	email = models.EmailField()
	uploaded_at = models.DateTimeField(auto_now_add=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True)

	class Meta:
		ordering = ["first_name"]

	def __str__(self):
		return self.username

class BusinessProfile(models.Model):
	user = models.OneToOneField(User, related_name="businessProfile", on_delete=models.CASCADE)
	type = models.CharField(max_length=50, choices=TYPECHOICES, default='business')
	username = models.CharField(max_length=150, blank=True)
	first_name = models.CharField(max_length=30, blank=True)
	last_name = models.CharField(max_length=30, blank=True)
	file = models.FileField(upload_to='profile_pictures/', null=True, blank=True)
	location = models.CharField(max_length=255, blank=True)
	tel = models.CharField(max_length=255, blank=True)
	description = models.TextField(blank=True)
	working_hours = models.CharField(max_length=255, blank=True)
	email = models.EmailField()
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["first_name"]

	def __str__(self):
		return self.username