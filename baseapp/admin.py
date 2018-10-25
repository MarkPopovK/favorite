from django.contrib import admin
from .models import Interest, Interested, Profile

# Register your models here.

admin.site.register(Interest)
admin.site.register(Interested)
admin.site.register(Profile)