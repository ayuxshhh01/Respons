from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from .serializer import *
from rest_framework.permissions import IsAuthenticated
from .serializer import LocationSerializer 
from rest_framework.views import APIView
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.utils import timezone
from datetime import timedelta
import math

# # Create your views here.
# @api_view()
# def home(request):
#   return Response(
#     {
#       'status':200,
#       'messege':'Yes Django rest is working'
#     }
#   )

# @api_view(['POST'])
# def get_home(request):
#   if request.method=="POST":
#     return Response({
#     'status':200,
#     'method':'Post',
#     'messegae':'Hello'
#   })


# @api_view(['GET','POST'])
# def post_todo(request):
#   try:
#     data=request.data
#     print(data)
#     return Response({
#       'status':200,
#       'messege':"Something went wrong"
#     })

#   except Exception as e:
#     print(e)
#   TodoSerializer



DANGER_ZONE = {'lat': 18.5204, 'lon': 73.8567, 'radius_km': 1} # Pune City Center

def is_in_danger_zone(lat, lon):
    # Simple distance calculation
    R = 6371 # Radius of earth in kilometers
    dLat = (lat - DANGER_ZONE['lat']) * math.pi / 180
    dLon = (lon - DANGER_ZONE['lon']) * math.pi / 180
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(DANGER_ZONE['lat'] * math.pi / 180) * math.cos(lat * math.pi / 180) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c
    return distance < DANGER_ZONE['radius_km']
# --- END OF SIMULATION LOGIC ---


class UpdateLocationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            now = timezone.now()
            location = serializer.validated_data

            # --- AI SIMULATION ---
            # 1. Check for "Prolonged inactivity"
            if user.last_location_update and now - user.last_location_update > timedelta(hours=1):
                Alert.objects.create(user=user, alert_type="Inactivity", location=location)
                print(f"INACTIVITY ALERT for {user.username}")

            # 2. Check for "Geo-fencing Alerts"
            if is_in_danger_zone(location['lat'], location['lon']):
                Alert.objects.create(user=user, alert_type="GeoFence", location=location)
                print(f"GEOFENCE ALERT for {user.username}")
            # --- END OF AI SIMULATION ---

            user.last_location_update = now
            user.save()

            return Response({"status": "location updated and checked"})
        return Response(serializer.errors, status=400)



class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

def check_geofence(lat, lon):
    
    all_zones = GeoZone.objects.all()
    for zone in all_zones:
        
        R = 6371 
        dLat = (lat - zone.center_lat) * math.pi / 180
        dLon = (lon - zone.center_lon) * math.pi / 180
        a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(zone.center_lat * math.pi / 180) * math.cos(lat * math.pi / 180) * math.sin(dLon/2) * math.sin(dLon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = R * c
        if distance < zone.radius_km:
            return True 
    return False


#view for realtime location
class UpdateLocationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            now = timezone.now()
            location = serializer.validated_data

            # --- UPGRADED AI SIMULATION ---
            # Check for "Prolonged inactivity"
            if user.last_location_update and now - user.last_location_update > timedelta(hours=1):
                Alert.objects.create(user=user, alert_type="Inactivity", location=location)
                print(f"INACTIVITY ALERT for {user.username}")

            # Check for "Geo-fencing Alerts" against the database
            if check_geofence(location['lat'], location['lon']):
                Alert.objects.create(user=user, alert_type="GeoFence", location=location)
                print(f"GEOFENCE ALERT for {user.username}")
            # --- END OF UPGRADED SIMULATION ---

            user.last_location_update = now
            user.save()

            return Response({"status": "location updated and checked"})
        return Response(serializer.errors, status=400)


class PanicAlertView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        location_serializer = LocationSerializer(data=request.data)
        if location_serializer.is_valid():
            alert = Alert.objects.create(
                user=user,
                alert_type="SOS",
                location=location_serializer.validated_data
            )
            print(f"PANIC ALERT for {user.username} at {alert.location}")

            # --- NEW REAL-TIME LOGIC ---
            channel_layer = get_channel_layer()
            alert_json = {
                'type': 'sos',
                'user': user.username,
                'location': alert.location,
                'timestamp': str(alert.timestamp)
            }
            async_to_sync(channel_layer.group_send)(
                'alerts_group',
                {
                    'type': 'send.alert', # This calls the send_alert method in your consumer
                    'alert': alert_json
                }
            )
            # --- END OF NEW LOGIC ---

            return Response({"status": "alert created and pushed", "alert_id": alert.id})
        return Response(location_serializer.errors, status=400)


class DashboardDataView(generics.ListAPIView):
    # For now, only staffand police can see the data.
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.filter(is_staff=False)
    serializer_class = DashboardUserSerializer


class ItineraryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # For now, we return a hardcoded itinerary.
        # Later, this can be powered by AI.
        mock_itinerary = {
            "destination": "Solapur, Maharashtra",
            "duration_days": 2,
            "plan": {
                "day_1": [
                    {"time": "10:00 AM", "activity": "Visit Siddheshwar Temple"},
                    {"time": "01:00 PM", "activity": "Lunch at a local restaurant"},
                    {"time": "03:00 PM", "activity": "Explore Bhuikot Fort"},
                ],
                "day_2": [
                    {"time": "11:00 AM", "activity": "Day trip to Pandharpur"},
                    {"time": "06:00 PM", "activity": "Return to Solapur"},
                ]
            }
        }
        return Response(mock_itinerary)