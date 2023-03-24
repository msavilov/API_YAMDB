from django.contrib import admin

from .models import User
from reviews.models import Review

admin.site.register(Review, User)
