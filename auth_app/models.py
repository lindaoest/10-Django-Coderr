from django.db import models

class CustomerProfile(models.Model):
	first_name = models.CharField(max_length=155)
	last_name = models.CharField(max_length=155)
	username = models.CharField(max_length=155)
	email = models.EmailField(max_length=366, unique=True)
	created_at = models.DateTimeField(auto_now_add=True)
	file = models.FileField(upload_to='profile/customer/')

class BusinessProfile(models.Model):
	first_name = models.CharField(max_length=155)
	last_name = models.CharField(max_length=155)
	username = models.CharField(max_length=155)
	description = models.TextField()
	email = models.EmailField(max_length=366, unique=True)
	created_at = models.DateTimeField(auto_now_add=True)
	file = models.FileField(upload_to='profile/business/')
	tel = models.IntegerField()
	location = models.CharField(max_length=366)
	working_hours = models.CharField(max_length=366)
