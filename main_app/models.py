from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profilePic = models.CharField()

    def __str__(self):
        return self.user.username

def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)

class Post(MPTTModel):
    author = models.ForeignKey(Profile, related_name='requests_created', on_delete=models.CASCADE)
    title = models.CharField(max_length = 50)
    text_body = models.TextField()
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE) 
    image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    likes = models.ManyToManyField(Profile, blank=True, related_name='likes_created')
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['-added']
        

class Follow(models.Model):
    follower = models.ForeignKey(Profile, related_name='follower_created', on_delete=models.CASCADE)
    isFollowing = models.ForeignKey(Profile, related_name='isfollowing_created', on_delete=models.CASCADE)


