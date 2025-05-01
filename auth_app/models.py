from django.db import models
from django.contrib.auth.models import User

TYPECHOICES = [
	("business", "Business"),
	("customer", "Customer")
]

class UserProfile(models.Model):
	user = models.OneToOneField(User, related_name="userProfile", on_delete=models.CASCADE)
	type = models.CharField(max_length=50, choices=TYPECHOICES, default='customer')

# class Profile(UserProfile):
# 	username = models.CharField(max_length=150)
# 	first_name = models.CharField(max_length=30)
# 	last_name = models.CharField(max_length=30)
# 	file = models.FileField(upload_to='profile_pictures/', null=True, blank=True)
# 	email = models.EmailField()

class CustomerProfile(models.Model):
	user = models.OneToOneField(User, related_name="customerProfile", on_delete=models.CASCADE)
	type = models.CharField(max_length=50, choices=TYPECHOICES, default='customer')
	username = models.CharField(max_length=150, blank=True)
	first_name = models.CharField(max_length=30, blank=True)
	last_name = models.CharField(max_length=30, blank=True)
	file = models.FileField(upload_to='profile_pictures/', null=True, blank=True)
	email = models.EmailField()
	uploaded_at = models.DateTimeField(auto_now_add=True)

class BusinessProfile(models.Model):
	user = models.OneToOneField(User, related_name="businessProfile", on_delete=models.CASCADE)
	type = models.CharField(max_length=50, choices=TYPECHOICES, default='customer')
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