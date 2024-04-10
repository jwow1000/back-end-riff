from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Post, Profile, Follow

admin.site.register(Post, MPTTModelAdmin)
admin.site.register(Profile)
admin.site.register(Follow)