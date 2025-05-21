from rest_framework import generics
from rest_framework import viewsets, status
from ..models import Order, Offer, Review, OfferDetail
from auth_app.models import BusinessProfile
from .serializers import OrderReadSerializer, OrderCreateSerializer, OrderUpdateSerializer, OfferReadSerializer, OfferCreateUpdateSerializer, OfferDetailSerializer, ReviewReadSerializer, ReviewCreateSerializer, ReviewUpdateSerializer
from rest_framework.permissions import AllowAny
from .permissions import ReviewPermission, OfferPermission, OrderPermission
from .pagination import OfferPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Avg
from rest_framework import filters
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ParseError

class OfferViewset(viewsets.ModelViewSet):
	queryset = Offer.objects.all()
	permission_classes = [OfferPermission]
	pagination_class = OfferPagination
	filter_backends = [filters.SearchFilter, filters.OrderingFilter]
	search_fields = ['title', 'description']
	ordering_fields = ['updated_at', 'min_price']

	# Return the appropriate serializer class depending on the HTTP method
	def get_serializer_class(self):
		if self.action in ['list', 'retrieve']:
			return OfferReadSerializer
		if self.action in ['create', 'partial_update', 'update']:
			return OfferCreateUpdateSerializer

	# Filter offers based on query parameters: max_delivery_time and creator_id
	def get_queryset(self):
		queryset = Offer.objects.all()

		max_delivery_time_param = self.request.query_params.get('max_delivery_time', None)

		if max_delivery_time_param is not None:
			try:
				if max_delivery_time_param:
					max_delivery_time_param = int(max_delivery_time_param)
					queryset = queryset.filter(details__delivery_time_in_days__lte=max_delivery_time_param).distinct()

			except (ValueError, TypeError):
				raise ParseError("Parameter 'max_delivery_time' muss eine Ganzzahl sein.")

		min_price_param = self.request.query_params.get('min_price', None)

		if min_price_param is not None:
			try:
				if min_price_param:
					min_price_param = int(min_price_param)
					queryset = queryset.filter(min_price__gte=min_price_param).distinct()

			except (ValueError, TypeError):
				raise ParseError("Parameter 'min_price' muss eine Ganzzahl sein.")

		creator_id_param = self.request.query_params.get('creator_id', None)

		if creator_id_param is not None:
			try:
				if creator_id_param:
					creator_id_param = int(creator_id_param)
					queryset = queryset.filter(user_id=creator_id_param)

			except (ValueError, TypeError):
				raise ParseError("Parameter 'creator_id' muss eine Ganzzahl sein.")

		return queryset

	# Set the current user as the creator of the offer
	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

class OfferDetailView(generics.RetrieveAPIView):
	queryset = OfferDetail.objects.all()
	serializer_class = OfferDetailSerializer
	permission_classes = [AllowAny]

class OrderViewset(viewsets.ModelViewSet):
	queryset = Order.objects.all()
	permission_classes = [OrderPermission]

	# Show orders based on user type (customer or business)
	def get_queryset(self):
		if hasattr(self.request.user, 'customerProfile'):
			user = get_object_or_404(User, pk=self.request.user.id)
			orders = Order.objects.filter(customer_user_id=user)
		elif hasattr(self.request.user, 'businessProfile'):
			user = get_object_or_404(User, pk=self.request.user.id)
			orders = Order.objects.filter(business_user_id=user)

		return orders

	# Return the appropriate serializer class depending on the HTTP method
	def get_serializer_class(self):
		if self.action in ['list', 'retrieve']:
			return OrderReadSerializer
		if self.action == 'create':
			return OrderCreateSerializer
		if self.action in ['partial_update', 'update']:
			return OrderUpdateSerializer

	# Handle the creation of a new order with proper validation
	def create(self, request, *args, **kwargs):
		serializer = OrderCreateSerializer(data=request.data, context={'request': request})
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderCountView(APIView):
	# Return the count of 'in_progress' orders for the given business user
	def get(self, request, business_user_id):
		get_object_or_404(User, pk=business_user_id)

		orders = Order.objects.filter(business_user_id=business_user_id, status='in_progress') # Filter orders by ID from the URL path and status 'in_progress'
		inProgressOrders = orders.count()

		return Response({
			'order_count': inProgressOrders
		})

class CompletedOrderCount(APIView):
	# Return the count of 'completed' orders for the given business user
	def get(self, request, business_user_id):
		get_object_or_404(User, pk=business_user_id)

		orders = Order.objects.filter(business_user_id=business_user_id, status='completed') # Filter orders by ID from the URL path and status 'completed'
		completedOrder = orders.count()

		return Response({
			'completed_order_count': completedOrder
		})

class ReviewViewset(viewsets.ModelViewSet):
	queryset = Review.objects.all()
	permission_classes = [ReviewPermission]
	filter_backends = [filters.OrderingFilter]
	ordering_fields = ['updated_at', 'rating']

	# Filter reviews based on business_user_id and reviewer_id query parameters
	def get_queryset(self):
		queryset = Review.objects.all()

		business_user_id = self.request.query_params.get('business_user_id', None)

		if business_user_id is not None:
			if business_user_id:
				queryset = queryset.filter(business_user_id=business_user_id)

		reviewer_id = self.request.query_params.get('reviewer_id', None)

		if reviewer_id is not None:
			if reviewer_id:
				queryset = queryset.filter(reviewer_id=reviewer_id)

		return queryset

	# Return the appropriate serializer class depending on the HTTP method
	def get_serializer_class(self):
		if self.action == 'list':
			return ReviewReadSerializer
		if self.action == 'create':
			return ReviewCreateSerializer
		if self.action == 'partial_update':
			return ReviewUpdateSerializer

	# Set the currently logged-in user as the reviewer
	def perform_create(self, serializer):
		customerprofile = User.objects.get(pk=self.request.user.id)
		serializer.save(reviewer=customerprofile)

class BaseInfoView(APIView):
	permission_classes = [AllowAny]

	# Return general statistics about offers, reviews, and business profiles
	def get(self, request):
		offers = Offer.objects.all()
		reviews = Review.objects.all()
		business_profiles = BusinessProfile.objects.all()

		averageRatings = Review.objects.aggregate(Avg('rating', default=0)) # Calculate average rating

		data = {
			'review_count': reviews.count(), # Count the total number of reviews in the database
			'average_rating': round(averageRatings['rating__avg'], 1), # Calculate the average rating, rounded to one decimal place
			'business_profile_count': business_profiles.count(), # Count the total number of business profiles
			'offer_count': offers.count() # Count the total number of offers
		}

		return Response(data)