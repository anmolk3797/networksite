from django.shortcuts import render
from .models import *
from .serializer import *
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import Permission
import requests

class SignUpView(viewsets.ModelViewSet):
    queryset           = User.objects.all()
    serializer_class   = UserSignUpSerializer
    def create(self,request):
        try :
            first_name            = request.data['first_name']
            last_name             = request.data['last_name']
            username              = request.data['username']
            password              = request.data['password']
            email                 = request.data['email']
            dob                   = request.data['dob']
            gender                = request.data['gender']
            emailre               = requests.get(f'https://emailvalidation.abstractapi.com/v1/?api_key=05127a895f414012a6e0fb3c71146037&email={email}')
            check_email           = emailre.json()
            email                 = check_email['is_valid_format']['value']
            if email==True:
                user = User.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    password=password,
                    email=request.data['email'],
                    dob=dob,
                    gender=gender,
                    )
                user.set_password(password)
                user.save()
                re                    = requests.get('https://ipgeolocation.abstractapi.com/v1/?api_key=244b5d59e96a4416a0d8235be2aef679')
                data                  = re.json()
                ip_address            = data['ip_address']
                country_code          = data ['country_code']
                user.save()
                year                  = user.date_joined.year
                month                 = user.date_joined.month
                day                   = user.date_joined.day
                hre                   = requests.get(f'https://holidays.abstractapi.com/v1/?api_key=da162cb223e64578bbe093aa98e0a029&country={country_code}&year={year}&month={month}&day={day}')
                holiday               = hre.json()
                user.ip_address       = ip_address,
                user.geolocation      = data['country'],
                user.holiday          = holiday
                user.save()
                context = {
                    "Message":"Signup successfully!!",
                    "status":200
                }
                return Response(context)
            else:
                context = {
                    "Message":"Please enter a valid email Address",
                    "status":400
                }
                return Response(context)
        except:
            return Response({"message":"User with this username is already exist."})

class LoginView(viewsets.ModelViewSet):
    queryset           = User.objects.all()
    serializer_class   = LoginSerializer

    def create(self,request):
        username = request.data['username']
        user=User.objects.get(username=username)
        if user:
            url = 'http://127.0.0.1:8000/api/token/'
            # token = Token.objects.create(user=user)
            # print(token.key)
            response = requests.post(url, 
            data={
                'username':request.data.get('username'),
                'password':request.data.get('password'),
            })
            re = response.json()
            context ={
                "message":"login Successfull!!!",
                "jwt_token":re
            }
            return Response(context)
        else:
            return Response({"invalid username or password"})

class PostView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset           = Post.objects.all()
    serializer_class   = PostSerializer
    def create(self, request):
        user=request.user
        post = request.data['post']
        Post.objects.create(post=post,post_creater=user)
        return Response({"message":"post created successfully!!"})


class LikesView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset           = Post.objects.all()
    def update(self, request, pk):
        post=Post.objects.get(id=pk)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            post.no_of_likes= post.no_of_likes-1
            post.save()
            return Response({"message":"You DisLiked this Post"})
        else:
            post.likes.add(request.user)
            post.no_of_likes= post.no_of_likes+1
            post.save()
            return Response({"message":"You Liked this Post"})
        return Response({"message":"Invalid Post"})


