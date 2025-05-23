from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OfferViewset, OfferDetailView, ReviewViewset, OrderViewset, OrderCountView, CompletedOrderCount, BaseInfoView

router = DefaultRouter()
router.register(r'offers', OfferViewset, basename='offer')
router.register(r'orders', OrderViewset, basename='order')
router.register(r'reviews', ReviewViewset, basename='review')

urlpatterns = [
	path('', include(router.urls)),
	path('offerdetails/<int:pk>/', OfferDetailView.as_view(), name='offer-detail'),
	path('order-count/<int:business_user_id>/', OrderCountView.as_view()),
	path('completed-order-count/<int:business_user_id>/', CompletedOrderCount.as_view()),
	path('base-info/', BaseInfoView.as_view()),
]