from django.urls import path
from .views import RegistrationView, LoginView, ProfileView, ProfileBusinessView, ProfileCustomerView


urlpatterns = [
	 path('registration/', RegistrationView.as_view()),
	 path('login/', LoginView.as_view()),
	 path('profile/<pk:int>/', ProfileView.as_view()),
	 path('profiles/business/', ProfileBusinessView.as_view()),
	 path('profiles/customer/', ProfileCustomerView.as_view()),
]