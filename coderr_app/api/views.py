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
		order = Order.objects.filter(business_user_id=business_user_id)
		allOrders = order.count()

		return Response({
			'order_count': allOrders
		})


class CompletedOrderCount(APIView):
	permission_classes = [AllowAny]

	def get(self, request, business_user_id):
		order = Order.objects.filter(business_user_id=business_user_id,status='completed')
		completedOrder = order.count()
		return Response({
			'completed_order_count': completedOrder
		})

class ReviewViewset(viewsets.ModelViewSet):
	queryset = Review.objects.all()
	permission_classes = [AllowAny]

	def get_serializer_class(self):
		print('test', self.action)
		if self.action == 'list':
			return ReviewReadSerializer
		if self.action == 'create':
			return ReviewCreateSerializer
		if self.action == 'partial_update':
			return ReviewUpdateSerializer

	def perform_create(self, serializer):
		customerprofile = CustomerProfile.objects.get(user_id=self.request.user.id)
		print(self.request.user.id)
		print(customerprofile)
		serializer.save(reviewer=customerprofile)

class BaseInfoView(generics.ListAPIView):
	queryset = BaseInfo.objects.all()
	serializer_class = BaseInfoSerializer
	permission_classes = [AllowAny]