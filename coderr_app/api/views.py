from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets

# Create your views here.
class OfferViewset(viewsets.ModelViewSet):
	pass

class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
	pass

class OrderViewset(viewsets.ModelViewSet):
	pass

class OrderCountView(generics.ListAPIView):
	pass

class CompletedOrderCount(generics.ListAPIView):
	pass

class ReviewViewset(viewsets.ModelViewSet):
	pass

class BaseInfoView(generics.ListAPIView):
	pass