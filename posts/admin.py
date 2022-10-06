from django.contrib import admin

from .models import Post, Comments, ThreadModel, UserProfile

admin.site.register([Post, Comments, ThreadModel, UserProfile])
# Register your models here.
