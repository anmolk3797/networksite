from django.contrib import admin
from .models import User, Post

class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ['username','first_name','email' ]

admin.site.register(User, UserAdmin)
admin.site.register(Post)