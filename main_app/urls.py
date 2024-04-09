from django.urls import path
from .views import Home, RemoveLikeFromPost, UserPosts, FollowsList, PostDetail, CreateUserView, LoginView, VerifyUserView, PostList, ProfileList, ProfileDetail,AddLikeToPost

urlpatterns = [
    path('', Home.as_view(), name='home'),

    path('users/register/', CreateUserView.as_view(), name='register'),
    path('users/login/', LoginView.as_view(), name='login'),
    path('users/token/refresh/', VerifyUserView.as_view(), name='token_refresh'),
    path('users/<int:id>/',ProfileDetail.as_view(), name = 'ProfileDetails'),
    path('users/', ProfileList.as_view(), name = 'ProfileList'), 
    
    path('posts/', PostList.as_view(), name = 'PostList'),
    path('posts/<int:id>/',PostDetail.as_view(), name = 'PostDetails'),
    path('profile/<int:id>/posts/', UserPosts.as_view(), name='userPosts'),

    path('follows/', FollowsList.as_view(), name='followsList'),
    
    path('posts/<int:post_id>/remove_like/<int:profile_id>', RemoveLikeFromPost.as_view(), name = 'remove-like-from-post'),
    path('posts/<int:post_id>/add_like/<int:profile_id>', AddLikeToPost.as_view(), name = 'add-like-to-post'),
]
