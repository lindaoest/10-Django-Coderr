from django.contrib import admin
from django.urls import path, include
from .views import OfferView

urlpatterns = [
	path('offers/', OfferView.as_view())
]