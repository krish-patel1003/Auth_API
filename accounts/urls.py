from django.urls import path
from accounts.views import RegisterAPIView, LoginAPIView, ProfileView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile')
] 