from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import registro

urlpatterns = [
    
    path('registro/',registro, name='registro'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]

