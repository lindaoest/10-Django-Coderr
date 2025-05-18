from django.contrib import admin
from .models import BusinessProfile, CustomerProfile

class CustomerAdmin(admin.ModelAdmin):
	list_filter = ["username"]
	list_display = ["username", "first_name", "last_name", "email"]

admin.site.register(BusinessProfile, CustomerAdmin)
admin.site.register(CustomerProfile, CustomerAdmin)