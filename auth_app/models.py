from django.db import models
from django.contrib.auth.models import User

TYPECHOICES = [
	("business", "Business"),
	("customer", "Customer")
]

class UserProfile(models.Model):
	user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
	username = models.CharField(max_length=150)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	file = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
	type = models.CharField(max_length=50, choices=TYPECHOICES, default='customer')
	email = models.EmailField()

class CustomerProfile(models.Model):
	user_profile = models.OneToOneField(UserProfile, related_name="customer_profile", on_delete=models.CASCADE)
	uploaded_at = models.DateTimeField(auto_now_add=True)

class BusinessProfile(models.Model):
	user_profile = models.OneToOneField(UserProfile, related_name="business_profile", on_delete=models.CASCADE)
	location = models.CharField(max_length=255)
	tel = models.CharField(max_length=255)
	description = models.TextField()
	working_hours = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)