from django.urls import path
from .views import RegistrationView, LoginView, ProfileDetailView, ProfileBusinessView, ProfileCustomerView

urlpatterns = [
	 path('registration/', RegistrationView.as_view()),
	 path('login/', LoginView.as_view()),
	 path('profile/<int:pk>/', ProfileDetailView.as_view()),
	 path('profiles/business/', ProfileBusinessView.as_view()),
	 path('profiles/customer/', ProfileCustomerView.as_view()),
]