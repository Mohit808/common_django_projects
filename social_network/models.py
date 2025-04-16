from django.db import models
from globalStoreApp.models import *

class Post(models.Model):
    user_id=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    text=models.TextField()
    image=models.TextField(null=True,blank=True)

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