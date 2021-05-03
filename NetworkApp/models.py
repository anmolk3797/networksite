import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username        = models.CharField(max_length=100, unique=True)
    password        = models.CharField(max_length=100, null=True, blank=True)
    email           = models.EmailField(null=True, blank=False, )
    first_name      = models.CharField(max_length=50, null=True, blank=False)
    last_name       = models.CharField(max_length=50, null=True, blank=True)
    dob             = models.DateField(null=True, blank=True)
    gender          = models.CharField(max_length=10, null=True, blank=True)
    ip_address      = models.CharField(max_length=100,null=True,blank=True)
    geolocation     = models.CharField(max_length=100,null=True,blank=True)
    holiday         = models.TextField(default=False)
    
class Post(models.Model):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post            = models.TextField(null=True, blank=True)
    post_creater    = models.ForeignKey(User,on_delete=models.CASCADE, related_name='post')
    likes           = models.ManyToManyField(User, blank=True, related_name='likes')
    no_of_likes     = models.IntegerField(default=0)
