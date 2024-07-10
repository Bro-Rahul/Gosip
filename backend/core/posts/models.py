from django.db import models
from users.models import *
from django.core.exceptions import ValidationError
# Create your models here.

class BasePost(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    body = models.TextField()

    class Meta:
        abstract = True

class Post(BasePost):
    created_by = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to="posts/images",null=True,blank=True)
    title = models.CharField(max_length=150,null=True,blank=True)

    def __str__(self) -> str:
        return f"{self.title} by the user {self.created_by.username}"
    


class Comment(BasePost):
    created_by = models.ForeignKey(Commenter, on_delete=models.CASCADE, related_name='comments')

    post = models.ForeignKey(Post,related_name="comments",on_delete=models.CASCADE)

    sub_comments = models.ForeignKey("self",on_delete=models.CASCADE, related_name='sub_comment',null=True,blank=True)

    def __str__(self) -> str:
        return f"comment on {self.post} {self.body} {self.created_by.username} "
    
    class Meta:
        ordering = ('pk',)


class Thread(models.Model):
    user_post = models.ForeignKey(Post, related_name="thread",on_delete=models.CASCADE)
    
    identity = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f"thread on {self.user_post} by {self.user_post.created_by.username} publisher"
    
    class Meta:
        unique_together = ('user_post','identity')


class CommentLikeDislike(models.Model):
    class Vote(models.TextChoices):
        LIKE = "LIKE","Like",
        DISLIKE = "DISLIKE","Dislike",

    vote = models.CharField(max_length=8,choices=Vote.choices)
    user = models.ForeignKey(Commenter,on_delete=models.CASCADE,related_name="votes")
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE,related_name="comment_vote")

    class Meta:
        unique_together = ('user','comment',)

    def __str__(self) -> str:
        return f"user {self.user.username} vote {self.vote} on {self.comment}"
