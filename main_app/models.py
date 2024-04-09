from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profilePic = models.CharField()

    def __str__(self):
        return self.user.username

class Post(models.Model):
    author = models.ForeignKey(Profile, related_name='requests_created', on_delete=models.CASCADE)
    title = models.CharField(max_length = 50)
    text_body = models.TextField()
    comments = models.ForeignKey('self', blank=True, on_delete=models.CASCADE) 
    visual = models.TextField()
    # likes
    likes = models.ManyToManyField(Profile, blank=True, related_name='likes_created')

    def __str__(self):
        return self.title

    # class Meta:
    #     ordering = ['-pub_date']

class Follow(models.Model):
    follower = models.ForeignKey(Profile, related_name='follower_created', on_delete=models.CASCADE)
    isFollowing = models.ForeignKey(Profile, related_name='isfollowing_created', on_delete=models.CASCADE)


