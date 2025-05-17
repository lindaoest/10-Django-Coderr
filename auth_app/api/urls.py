from django.urls import path
from .views import RegistrationView, LoginView, ProfileDetailView, ProfileBusinessView, ProfileCustomerView

urlpatterns = [
	 path('registration/', RegistrationView.as_view(), name='registration-list'),
	 path('login/', LoginView.as_view(), name='login-list'),
	 path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
	 path('profiles/business/', ProfileBusinessView.as_view()),
	 path('profiles/customer/', ProfileCustomerView.as_view()),
]