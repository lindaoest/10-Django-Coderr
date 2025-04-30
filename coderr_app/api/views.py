from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from ..models import Order
from .serializers import OrderSerializer
from rest_framework.permissions import AllowAny

# Create your views here.
class OfferViewset(viewsets.ModelViewSet):
	pass

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
	pass

class BaseInfoView(generics.ListAPIView):
	pass