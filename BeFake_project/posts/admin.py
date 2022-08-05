from django.contrib import admin

from .models import Post, Comments, ThreadModel

admin.site.register([Post, Comments, ThreadModel])
# Register your models here.
