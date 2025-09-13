from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from .serializer import *
from rest_framework.permissions import IsAuthenticated
from .serializer import LocationSerializer 
from rest_framework.views import APIView

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




class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer




#view for realtime location
class UpdateLocationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
           
            print(f"User {request.user.username} is at {serializer.validated_data}")
            return Response({"status": "location updated"})
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
            # We will add the real-time push notification here on Day 3.
            return Response({"status": "alert created", "alert_id": alert.id})
        return Response(location_serializer.errors, status=400)


class DashboardDataView(generics.ListAPIView):
    # For now, only staffand police can see the data.
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.filter(is_staff=False)
    serializer_class = DashboardUserSerializer