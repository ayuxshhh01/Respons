from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from .serializer import *

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