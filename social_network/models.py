from django.db import models
from globalStoreApp.models import *

class Post(models.Model):
    user_id=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    text=models.TextField(blank=True, null=True)  # Post content
    image=models.TextField(null=True,blank=True)
    location=models.CharField(max_length=255,null=True,blank=True)
    latitude=models.FloatField(null=True,blank=True)
    longitude=models.FloatField(null=True,blank=True)
    tags=models.CharField(max_length=255,null=True,blank=True)  # Comma-separated tags
    people_tagged=models.ManyToManyField(Customer, related_name='tagged_posts', blank=True)
    description=models.TextField(null=True,blank=True)  
    can_reply=models.IntegerField(null=True,blank=True)  # Whether replies are allowed
    is_public=models.BooleanField(default=True)  # Public or private post
    likes_count=models.PositiveIntegerField(default=0)  # Count of likes
    comments_count=models.PositiveIntegerField(default=0)  # Count of comments
    retweet_count=models.PositiveIntegerField(default=0)  # Count of shares
    is_deleted=models.BooleanField(default=False)  # Soft delete flag
    is_reported=models.BooleanField(default=False)  # Flag for reported posts
    is_archived=models.BooleanField(default=False)  # Flag for archived posts
    created_at=models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text


class Like(models.Model):
    user_id=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    post_id=models.ForeignKey(Post,on_delete=models.CASCADE)


class Comment(models.Model):
    user_id=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    post_id=models.ForeignKey(Post,on_delete=models.CASCADE)
    text=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')


class Follow(models.Model):
    follower = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')  # Prevents duplicate follow relationships

    def __str__(self):
        return f"{self.follower} follows {self.following}"