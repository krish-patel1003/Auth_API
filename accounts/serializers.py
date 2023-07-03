from django.db.models import fields
from rest_framework import serializers
from rest_framework.utils import model_meta
from accounts.models import User, Profile
from django.contrib import auth
from rest_framework import exceptions
from django.contrib.auth.password_validation import validate_password

class RegisterSerializer(serializers.ModelSerializer):
    '''
    Registration Serializer
    '''

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', )
        extra_kwargs = {'password': {'write_only': True}}
    
    def validate(self, attrs):
        '''
        validate method - validates the instance passed to the serializer
        '''

        username = attrs.get('username', '')
        password = attrs.get('password', '')

        if not username.isalnum():
            raise serializers.ValidationError("Username should be alphnumeric")

        try:
             # validate the password and catch the exception
            validate_password(password=password, user=self.instance)
         
         # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(str(e))
        
        return attrs
    

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.ModelSerializer):
    '''
    Login serializer
    '''
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(min_length=1, write_only=True)
    tokens = serializers.SerializerMethodField()
    
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'tokens')
    
    def get_tokens(self, instance):
        '''
        returns the object returned by tokens method in AUTH_USER_MODEL
        '''

        user = User.objects.get(email=instance['email'])
        
        return {
            "refresh_token": user.tokens()['refresh_token'],
            "access_token": user.tokens()["access_token"]
        }

    
    def validate(self, attrs):
        '''
        validate method - validates the instance passed to the serializer
        '''

        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)

        if not user:
            raise exceptions.AuthenticationFailed('Invalid credentials, try again')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('Account Disabled, contact admin')

        return {
            "id":user.id,
            "email": user.email,
            "username": user.username,
            "tokens": user.tokens
        }


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ("id", "user", "first_name", "last_name", "bio")
        extra_kwargs = {"user": {"read_only": True}}
