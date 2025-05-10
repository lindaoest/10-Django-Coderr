from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets, status
from ..models import Order, Offer, Review, BaseInfo, OfferDetail
from auth_app.models import BusinessProfile, CustomerProfile
from .serializers import OrderSerializer, OrderPostSerializer, OrderPutSerializer, OfferSerializer, OfferDetailSerializer, ReviewReadSerializer, ReviewCreateSerializer, ReviewUpdateSerializer, BaseInfoSerializer
from rest_framework.permissions import AllowAny
from .pagination import OfferPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Avg

# Create your views here.
class OfferViewset(viewsets.ModelViewSet):
	queryset = Offer.objects.all()
	serializer_class = OfferSerializer
	permission_classes = [AllowAny]
	pagination_class = OfferPagination

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

	# def get_queryset(self):
	# 	if hasattr(self.request.user, 'businessProfile'):
	# 		offers = Offer.objects.filter(user_id=self.request.user)

	# 	return offers

class OfferDetailView(generics.RetrieveAPIView):
	queryset = OfferDetail.objects.all()
	serializer_class = OfferDetailSerializer
	permission_classes = [AllowAny]

class OrderViewset(viewsets.ModelViewSet):
	queryset = Order.objects.all()
	permission_classes = [AllowAny]

	def get_queryset(self):
		if hasattr(self.request.user, 'customerProfile'):
			user = CustomerProfile.objects.get(user_id=self.request.user.id)
			orders = Order.objects.filter(customer_user_id=user)
		elif hasattr(self.request.user, 'businessProfile'):
			user = BusinessProfile.objects.get(user_id=self.request.user.id)
			orders = Order.objects.filter(business_user_id=user)

		return orders

	def get_serializer_class(self):
		if self.action == 'list' or 'retrieve':
			return OrderSerializer
		if self.action == 'create':
			return OrderPostSerializer
		if self.action == 'partial_update' or 'update':
			return OrderPutSerializer

	def create(self, request, *args, **kwargs):
		serializer = OrderPostSerializer(data=request.data, context={'request': request})
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderCountView(APIView):
	permission_classes = [AllowAny]

	def get(self, request, business_user_id):
		orders = Order.objects.filter(business_user_id=business_user_id, status='in_progress')
		inProgressOrders = orders.count()

		return Response({
			'order_count': inProgressOrders
		})


class CompletedOrderCount(APIView):
	permission_classes = [AllowAny]

	def get(self, request, business_user_id):
		orders = Order.objects.filter(business_user_id=business_user_id, status='completed')
		completedOrder = orders.count()
		return Response({
			'completed_order_count': completedOrder
		})

class ReviewViewset(viewsets.ModelViewSet):
	queryset = Review.objects.all()
	permission_classes = [AllowAny]

	def get_serializer_class(self):
		if self.action == 'list':
			return ReviewReadSerializer
		if self.action == 'create':
			return ReviewCreateSerializer
		if self.action == 'partial_update':
			return ReviewUpdateSerializer

	def perform_create(self, request, serializer):
		customerprofile = CustomerProfile.objects.get(user_id=self.request.user.id)
		serializer.save(reviewer=customerprofile)

class BaseInfoView(APIView):

	def get(self, request):
		offers = Offer.objects.all()
		reviews = Review.objects.all()
		business_profiles = BusinessProfile.objects.all()
		averageRatings = Review.objects.aggregate(Avg('rating', default=0))

		data = {
			'review_count': reviews.count(),
			'average_rating': round(averageRatings['rating__avg'], 1),
			'business_profile_count': business_profiles.count(),
			'offer_count': offers.count()
		}

		return Response(data)