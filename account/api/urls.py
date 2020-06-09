from django.urls import path,include
from agreement.api import views
from rest_framework.authtoken.views import obtain_auth_token 
app_name='account'

urlpatterns = [
    #path('api-auth/', include('rest_framework.urls')),
    path('login', obtain_auth_token, name='account_login'),
]