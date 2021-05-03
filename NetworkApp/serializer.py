from rest_framework import serializers
from .models import *

class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = "__all__"

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ['username','password']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Post
        fields = "__all__"
