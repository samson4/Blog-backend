from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import NewUser,Profile

# Register your models here.
admin.site.register(NewUser)
admin.site.register(Profile)