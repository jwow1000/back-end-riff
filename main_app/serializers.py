from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Post, Profile, Follow
from rest_framework.validators import UniqueValidator

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )

        return user

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):  
    likes = ProfileSerializer(many=True, read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # Make the user field read-only
    image = serializers.ImageField(required=True)
    class Meta:
        model = Post
        fields = '__all__'
        
class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'