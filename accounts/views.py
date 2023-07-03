from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from accounts.models import Profile
from accounts.serializers import RegisterSerializer, LoginSerializer, ProfileSerializer
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsProfileOwner


class RegisterAPIView(GenericAPIView):
    '''
    Register View - handles user registration
    '''

    serializer_class = RegisterSerializer
    authentication_classes = []

    def post(self, request):

        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if request.data.get('is_organization', False):
            return Response(
                {"data": serializer.data, "msg":"new organization registered"}, status=status.HTTP_201_CREATED)

        return Response(
            {"data": serializer.data, "mssg": "new user registerd"}, status=status.HTTP_201_CREATED)


class LoginAPIView(GenericAPIView):
    '''
    Login View - handles login
    '''
        
    serializer_class = LoginSerializer
    authentication_classes = []

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(
            {"data": serializer.data, "mssg": "user logged in"}, status=status.HTTP_200_OK)


class ProfileView(GenericAPIView):

    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsProfileOwner]

    def get(self, request):

        logged_in_user = request.user
        profile = Profile.objects.get(user=logged_in_user)

        if not profile.exists():
            return Response(
                {"error": "No Profile Found for the logged in User"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.serializer_class(instance=profile)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    

    def put(self, request):

        logged_in_user = request.user
        profile = Profile.objects.get(user=logged_in_user)

        if not profile.exists():
            return Response(
                {"error": "No Profile Found for the logged in User"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.serializer_class(
            data=request.data, instance=profile)
        
        if serializer.is_valid():
            return Response(
                {"data": serializer.data, "message":"profile updated"}, 
                status=status.HTTP_200_OK
            )
        
        return Response(
            {"Error": serializer.errors}, 
            status=status.HTTP_400_BAD_REQUEST
        )

