from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from ..models import Order, Offer, Review
from .serializers import OrderSerializer, OfferSerializer, ReviewSerializer
from rest_framework.permissions import AllowAny

# Create your views here.
class OfferViewset(viewsets.ModelViewSet):
	queryset = Offer.objects.all()
	serializer_class = OfferSerializer
	permission_classes = [AllowAny]

class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
	pass

class OrderViewset(viewsets.ModelViewSet):
	queryset = Order.objects.all()
	serializer_class = OrderSerializer
	permission_classes = [AllowAny]

class OrderCountView(generics.ListAPIView):
	pass

class CompletedOrderCount(generics.ListAPIView):
	pass

class ReviewViewset(viewsets.ModelViewSet):
	queryset = Review.objects.all()
	serializer_class = ReviewSerializer
	permission_classes = [AllowAny]

class BaseInfoView(generics.ListAPIView):
	pass