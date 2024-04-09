from django.contrib import admin
from .models import Post, Profile, Follow

admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Follow)