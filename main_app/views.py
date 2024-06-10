from django.http import Http404
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions 
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Post, Profile, Follow, User
from .serializers import UserSerializer, ProfileSerializer, FollowSerializer, PostSerializer 

# Home
class Home(APIView):
    def get(self, request):
        content = {'message': 'Welcome to the Riff api home route!'}
        return Response(content)
    
# User Creation and Auth
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self,request,*args,**kwargs):
        response = super().create(request,*args,**kwargs)
        user = User.objects.get(username=response.data['username'])
        refresh = RefreshToken.for_user(user)

        print(request.data.get('profilePic'))
        profile_data = request.data.get('profilePic')
        profile = Profile.objects.create(user=user, profilePic=profile_data)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': response.data,
            'profile': ProfileSerializer(profile).data
        })

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:

            profile = Profile.objects.get(user=user)
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data, 
                'profile': ProfileSerializer(profile).data
            })
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class VerifyUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = User.objects.get(username=request.user)  # Fetch user profile
        profile = Profile.objects.get(user=user)
        refresh = RefreshToken.for_user(request.user)  # Generate new refresh token
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data,
            'profile': ProfileSerializer(profile).data
        })    

#Profile creation and Edit
class ProfileList(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]  # Ensure user is authenticated

    def get_object(self):
        user_id = self.kwargs.get('id')  # Get the user ID from URL
        try:
            profile = Profile.objects.get(user__id=user_id)
            self.check_object_permissions(self.request, profile)  # Check permissions against the profile
            return profile
        except Profile.DoesNotExist:
            raise Http404

    def perform_update(self, serializer):
        profile = self.get_object()
        if profile.user != self.request.user:
            raise PermissionDenied({"message": "You do not have permission to edit this profile."})
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied({"message": "You do not have permission to delete this profile."})
        instance.delete()

#Post create and edit
class PostList(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)  
    def get_queryset(self):
        return Post.objects.all()

    def perform_create(self, serializer):
        profile = Profile.objects.get(user__id=self.request.user.id)
        serializer.save(author=profile)

class PostDetail(generics.RetrieveUpdateDestroyAPIView): 
    serializer_class = PostSerializer
    lookup_field = 'id'
    queryset = Post.objects.all()

# get all child comments by parent id
class PostComments(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    def get_queryset(self):
        post_id = self.kwargs['id']
        return Post.objects.filter(parent = post_id)
    def perform_create(self, serializer):
        post_id = self.kwargs['id']
        post = Post.objects.get(id = post_id)
        serializer.save(post=post)

#Likes 
class AddLikeToPost(APIView):
    def post(self, request, post_id, profile_id):
        post = Post.objects.get(id = post_id)
        profile = Profile.objects.get(id = profile_id)
        post.likes.add(profile)
        return Response({'message': f'{profile.user.username} liked this post.'})
     
class RemoveLikeFromPost(APIView):
    def delete(self, request, post_id, profile_id):
        post = Post.objects.get(id = post_id)
        profile = Profile.objects.get(id = profile_id)
        post.likes.remove(profile)
        return Response({'message': f'{profile.user.username} unliked this post.'})

#Get all posts by one profile
class UserPosts(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    def get_queryset(self):
        profile_id = self.kwargs['id']
        return Post.objects.filter(author = profile_id)
    def perform_create(self,serializer):
        profile_id = self.kwargs['id']
        profile = Profile.objects.get(id = profile_id)
        serializer.save(profile = profile)

#Followers
class AddFollower(generics.ListCreateAPIView):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]  

    def get_queryset(self):
        return Follow.objects.all()

    def perform_create(self, serializer):
        profile = Profile.objects.get(user__id=self.request.user.id)
        is_following_id = self.request.data.get('isFollowing')
        serializer.save(follower=profile, isFollowing_id=is_following_id)

# class RemoveFollower(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = FollowSerializer
#     lookup_field = 'id'
#     queryset = Follow.objects.all()

class RemoveFollower(generics.GenericAPIView):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, id):
        # Fetch the profile of the logged-in user
        user_profile = get_object_or_404(Profile, user=request.user)

        # Attempt to retrieve the follow relationship
        follow = get_object_or_404(Follow, follower=user_profile, isFollowing__id=id)

        # Delete the follow relationship
        follow.delete()

        # Return a response indicating the follow was deleted
        return Response({"message": "Follow relationship deleted."}, status=status.HTTP_204_NO_CONTENT)

#Get list of all followed profiles 
class FollowsList(generics.ListCreateAPIView):
    serializer_class = FollowSerializer
    lookup_field = 'profile_id'
  
    def get_queryset(self):
        profile_id = self.kwargs['profile_id']
        return Follow.objects.filter(follower = profile_id)
    def perform_create(self,serializer):
        profile_id = self.kwargs['profile_id']
        profile = Profile.objects.get(id = profile_id)
        serializer.save(profile = profile)

#get all posts by fav users
# class FavUserPosts(generics.ListCreateAPIView):
#     serializer_class = PostSerializer
#     lookup_field = 'profile_id'

#     def get_queryset(self):
#         profile_id = self.kwargs['profile_id']
#         favProfs = Follow.objects.filter(follower = profile_id)
#         return Post.objects.filter(author=favProfs)
#     def perform_create(self,serializer):
#         profile_id = self.kwargs['profile_id']
#         profile = Profile.objects.get(id = profile_id)
#         serializer.save(profile = profile)
    
    
class FavUserPosts(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        # Retrieve the profile ID from the URL
        profile_id = self.kwargs['profile_id']

        # Get the profiles that are being followed by the profile with the given profile_id
        # We use 'follower__id' to specify the field in the Follow model we are filtering against
        followed_profiles = Follow.objects.filter(follower__id=profile_id).values_list('isFollowing__id', flat=True)

        # Fetch posts where the author's profile ID is in the list of followed profiles
        return Post.objects.filter(author__id__in=followed_profiles)    