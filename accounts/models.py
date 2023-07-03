from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from accounts.managers import UserManager
from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractBaseUser, PermissionsMixin):
    '''
    Custom AUTH_USER_MODEL.
    '''

    username = models.CharField(max_length=255, unique=True, null=False, db_index=True)
    email = models.EmailField(max_length=255, unique=True, null=False, db_index=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        '''
        returns a string - "<username>".
        '''
        
        return self.username
    
    def tokens(self):
        '''
        returns a object - containing refresh_token and access_token.
        '''

        refresh_token = RefreshToken.for_user(self)
        return {
            'refresh_token':str(refresh_token),
            'access_token':str(refresh_token.access_token)
        }


class Profile(models.Model):
    '''
    Profile Model.
    '''

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_profile")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField()

    def __str__(self) -> str:
        return f'{self.user.username} {self.first_name}'
    
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'