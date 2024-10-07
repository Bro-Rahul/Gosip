from rest_framework import serializers
from django.db import transaction
from django.utils import timesince,timezone
from users.models import *
from .models import *



class BaseCommentSerializer(serializers.ModelSerializer):
    sub_comments = serializers.SerializerMethodField(read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(queryset=Commenter.commenter.all())
    user = serializers.SerializerMethodField(read_only=True)
    profile = serializers.SerializerMethodField(read_only=True)
    time_period = serializers.SerializerMethodField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    vote = serializers.SerializerMethodField(read_only=True)
    like = serializers.SerializerMethodField(read_only=True)
    dislike = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model = Comment
        fields = '__all__'


    def get_sub_comments(self, obj):
        sub_comments = obj.sub_comment.all()
        data = [comment.pk for comment in sub_comments]
        return data

    def get_user(self, obj):
        return obj.created_by.username

    def get_profile(self, obj):
        return obj.created_by.avatar.url if obj.created_by.avatar else None

    def get_time_period(self, obj):
        return timesince.timesince(obj.created_at, timezone.now())
    
    def get_vote(self,obj):
        try:
            login_user_id = self.context.get('user')
            if not login_user_id:
                return None    
            else:
                return obj.comment_vote.get(comment = obj.pk,user = login_user_id).vote
        except CommentLikeDislike.DoesNotExist:
            return None

    def get_like(self,obj):
        try:
            likes = obj.comment_vote.all().filter(vote="LIKE").count()
            return likes
        except CommentLikeDislike.DoesNotExist:
            return 0
    def get_dislike(self,obj):
        try:
            dislike = obj.comment_vote.all().filter(vote="DISLIKE").count()
            return dislike
        except CommentLikeDislike.DoesNotExist:
            return 0

class CommentSerializer(BaseCommentSerializer):
    class Meta(BaseCommentSerializer.Meta):
        pass

class ReplyOnCommentSerializer(BaseCommentSerializer):
    reply = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), write_only=True)

    class Meta(BaseCommentSerializer.Meta):
        pass

    def create(self, validated_data):
        main_comment = validated_data.pop('reply', None)
        comment = Comment.objects.create(**validated_data)
        comment.sub_comments = main_comment
        comment.save()
        return comment

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True,read_only=True)

    created_by = serializers.PrimaryKeyRelatedField(queryset = Publisher.publisher.all())

    class Meta:
        model = Post
        fields = ['id','body','comments','title','image','created_by']


class ThreadSerializer(serializers.ModelSerializer):
    user_post = PostSerializer(read_only=True)
    identity = serializers.CharField()
    body = serializers.CharField(write_only=True)
    title = serializers.CharField(write_only=True)
    image = serializers.ImageField(write_only=True,allow_null=True, required=False)
    created_by = serializers.PrimaryKeyRelatedField(queryset = Publisher.publisher.all(),write_only=True)

    class Meta:
        model = Thread
        fields = ['user_post','identity','body','title','image','created_by']
    
    def create(self, validated_data):
        post = {
            'created_by' : validated_data.pop('created_by',None),
            'body' : validated_data.pop('body',None),
            'title' : validated_data.pop('title',None),
            'image' : validated_data.pop('image',None)
        }
        try:
            with transaction.atomic():
                new_post = Post.objects.create(**post)
                thread = Thread.objects.create(user_post=new_post, **validated_data)
                return thread
        except ValidationError as e:
            raise ValidationError(e.message)
        
class CommentLikeDisLikeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset = Commenter.commenter.all())
    class Meta:
        model = CommentLikeDislike
        fields = '__all__'
