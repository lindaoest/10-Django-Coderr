from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from ..models import Order, Offer, Review, BaseInfo, OfferDetail
from auth_app.models import BusinessProfile
from .serializers import OrderSerializer, OfferSerializer, OfferDetailSerializer, ReviewSerializer, BaseInfoSerializer
from rest_framework.permissions import AllowAny
from .pagination import OfferPagination
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class OfferViewset(viewsets.ModelViewSet):
	queryset = Offer.objects.all()
	serializer_class = OfferSerializer
	permission_classes = [AllowAny]
	pagination_class = OfferPagination

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

class OfferDetailView(generics.RetrieveAPIView):
	queryset = OfferDetail.objects.all()
	serializer_class = OfferDetailSerializer
	permission_classes = [AllowAny]

class OrderViewset(viewsets.ModelViewSet):
	queryset = Order.objects.all()
	serializer_class = OrderSerializer
	permission_classes = [AllowAny]

class OrderCountView(APIView):
	permission_classes = [AllowAny]

	def get(self, request, business_user_id):
		orders = 0
		user = BusinessProfile.objects.get(user_id=business_user_id)
		orders = user.orders.count()

		return Response({
			'order_count': orders
		})


class CompletedOrderCount(generics.ListAPIView):
	pass

class ReviewViewset(viewsets.ModelViewSet):
	queryset = Review.objects.all()
	serializer_class = ReviewSerializer
	permission_classes = [AllowAny]

class BaseInfoView(generics.ListAPIView):
	queryset = BaseInfo.objects.all()
	serializer_class = BaseInfoSerializer
	permission_classes = [AllowAny]