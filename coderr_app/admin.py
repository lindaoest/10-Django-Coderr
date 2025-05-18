from django.contrib import admin
from .models import Offer, OfferDetail, Review

class CustomerOfferAdmin(admin.ModelAdmin):
	list_filter = ["title"]
	list_display = ["title", "user"]

	readonly_fields = ["min_price", "min_delivery_time"]

class CustomerOfferDetailAdmin(admin.ModelAdmin):
	list_filter = ["title", "offer"]
	list_display = ["title", "offer"]

class CustomerReviewAdmin(admin.ModelAdmin):
	list_filter = ["description"]
	list_display = ["description", "reviewer", "rating"]

admin.site.register(Offer, CustomerOfferAdmin)
admin.site.register(OfferDetail, CustomerOfferDetailAdmin)
admin.site.register(Review, CustomerReviewAdmin)
