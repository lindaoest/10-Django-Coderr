from django.db import models
from django.contrib.auth.models import User

TYPECHOICES = [
	("business", "Business"),
	("customer", "Customer")
]

class UserProf(models.Model):
	user = models.OneToOneField(User, related_name="userProfile", on_delete=models.CASCADE)
	type = models.CharField(max_length=50, choices=TYPECHOICES, default='customer')

class Profile(models.Model):
	user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
	username = models.CharField(max_length=150)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	file = models.FileField(upload_to='profile_pictures/', null=True, blank=True)
	type = models.CharField(max_length=50, choices=TYPECHOICES, default='customer')
	email = models.EmailField()

class CustomerProfile(Profile):
	uploaded_at = models.DateTimeField(auto_now_add=True)

class BusinessProfile(Profile):
	location = models.CharField(max_length=255)
	tel = models.CharField(max_length=255)
	description = models.TextField()
	working_hours = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)