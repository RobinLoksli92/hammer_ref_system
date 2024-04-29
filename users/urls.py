from django.urls import path, include

from .views import UserProfileView, PhoneNumberLoginView


urlpatterns = [
    path('auth/', PhoneNumberLoginView.as_view(), name='phone-auth'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]