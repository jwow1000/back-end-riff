from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import Home, PostComments, AddFollower, RemoveFollower, RemoveLikeFromPost, UserPosts, FollowsList, PostDetail, CreateUserView, LoginView, VerifyUserView, PostList, ProfileList, ProfileDetail, AddLikeToPost

urlpatterns = [
    path('', Home.as_view(), name='home'),

    path('users/register/', CreateUserView.as_view(), name='register'),
    path('users/login/', LoginView.as_view(), name='login'),
    path('users/token/refresh/', VerifyUserView.as_view(), name='tokenRefresh'),
    path('users/<int:id>/',ProfileDetail.as_view(), name = 'profileDetails'),
    path('users/', ProfileList.as_view(), name = 'profileList'), 
    
    path('posts/', PostList.as_view(), name = 'postList'),
    path('posts/<int:id>/',PostDetail.as_view(), name = 'postDetails'),
    path('posts/<int:id>/comments/', PostComments.as_view(), name = 'postComments'),
    path('profile/<int:id>/posts/', UserPosts.as_view(), name='userPosts'),

    path('follows/', AddFollower.as_view(), name='addFollower'),
    path('follows/<int:id>/', RemoveFollower.as_view(), name='removeFollower'),
    path('follows/<int:profile_id>/users/', FollowsList.as_view(), name='followsList'),
    
    path('posts/<int:post_id>/remove_like/<int:profile_id>/', RemoveLikeFromPost.as_view(), name = 'removeLikeFromPost'),
    path('posts/<int:post_id>/add_like/<int:profile_id>/', AddLikeToPost.as_view(), name = 'addLikeToPost'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
