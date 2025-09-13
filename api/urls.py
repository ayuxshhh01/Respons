
from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token # Import this


urlpatterns = [
  path('register/', RegisterView.as_view(), name='register'),
  path('login/', obtain_auth_token, name='login'),
  path('location/update/', UpdateLocationView.as_view(), name='update-location'),
  path('alerts/panic/', PanicAlertView.as_view(), name='panic-alert'),
  path('dashboard/data/', DashboardDataView.as_view(), name='dashboard-data'),
]
