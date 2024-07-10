from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from .permissions import VerifySecretKey,CommentorCreatorOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Q
from .serializers import *
from .models import *


# Create your views here.
class ThreadView(ViewSet):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer

    def list(self,request):
        serializer = self.serializer_class(self.queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def create(self,request):
        try:
            data = request.data
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)        
        except ValidationError as e:
            return Response({'info':e.message},status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'info' : 'can not create a new thread for some reason !'},status=status.HTTP_406_NOT_ACCEPTABLE)
    
    @action(detail=False, methods=['POST'], url_path="get-comments")
    def get_comments(self,request):
        secret_key = request.data.get('key',None)
        post = request.data.get('post',None)
        contains = Publisher.publisher.filter(secret_key__key = secret_key).exists()
        if contains:
            identify = request.data.get('identity',None)
            data = Thread.objects.filter(Q(user_post__created_by__secret_key__key = secret_key) & Q(identity=identify))
            print(data.count())
            if data.count()!=0:
                serializer = ThreadSerializer(data,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:                
                if not post:
                    return Response({'please provide meta data for the new post '},status=status.HTTP_400_BAD_REQUEST)
                publisher = Publisher.publisher.get(secret_key__key = secret_key)
                post['created_by'] = publisher.pk
                new_post_data = {
                    'identity' : identify,
                    **post
                }
                newpost_serializer = ThreadSerializer(data=new_post_data)
                if newpost_serializer.is_valid():
                    newpost_serializer.save()
                    print("created a new thread ")
                    return Response(newpost_serializer.data,status=status.HTTP_200_OK)
                else:
                    print("error")
                    print(newpost_serializer.errors)
                    return Response(newpost_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else:    
            return Response({'info':'Invalid secret Key'},status=status.HTTP_400_BAD_REQUEST)

        
        

    
class PostView(ViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    model = Post

    def list(self,request):
        serializer = self.serializer_class(self.queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def create(self,request):
        try:
            data = request.data
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({'info' : e.message},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'info' : 'can not create a post the request thread for some reason !'},status=status.HTTP_406_NOT_ACCEPTABLE)
    
    def update(self,request,pk=None):
        try:
            post = self.model.objects.get(pk=pk)
            #self.check_object_permissions(request,post)
        except self.model.DoesNotExist as e:
            return Response({'info':'no such post exits '},status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(post,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def destroy(self,request,pk=None):
        try:
            post = self.model.objects.get(pk=pk)
            #self.check_object_permissions(request,post)
        except self.model.DoesNotExist as e:
            return Response({'info' : 'no such post exits'},status=status.HTTP_400_BAD_REQUEST)
        post.delete()
        return Response({'info':'post has been deleted successfully'},status=status.HTTP_200_OK)
    

class CommentView(ViewSet):
    model = Comment
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.request.method in ['GET','POST']:
            self.permission_classes = [IsAuthenticated]
        elif self.request.method in ['DELETE','PUT','PATCH']:
            self.permission_classes = [IsAuthenticated,CommentorCreatorOrReadOnly]
        return super().get_permissions()
    
    def list(self,request):
        serializer = self.serializer_class(self.queryset,many=True)
        return Response(serializer.data)
    
    def create(self,request):
        try:
            data = request.data
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({'info': e.message},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'info' : 'can not create a post the request thread for some reason !'},status=status.HTTP_406_NOT_ACCEPTABLE)
    
    @action(methods=['POST'],detail=False,url_path="comment-reply")
    def add_subcomment(self,request):
        data = request.data
        try:
            serializer = ReplyOnCommentSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({'info': e.message},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'info' : 'can not create a post the request thread for some reason !'},status=status.HTTP_406_NOT_ACCEPTABLE)
        

    @action(methods=["PUT","PATCH"],detail=True,url_path="update-user-comment")
    def update_user_comment(self,request,pk=None):
        try:
            comment = self.model.objects.get(pk=pk)
            self.check_object_permissions(request,comment)
        except self.model.DoesNotExist as e:
            return Response({'info':'no such comment exits '},status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(comment,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    @action(methods=["DELETE"],detail=True,url_path="delete-comment")
    def delete_comment(self,request,pk=None):
        try:
            comment = self.model.objects.get(pk=int(pk))
            self.check_object_permissions(request,comment)
        except self.model.DoesNotExist as e:
            return Response({'info' : 'no such comment exits'},status=status.HTTP_400_BAD_REQUEST)
        comment.delete()
        return Response({'info':'comment has been deleted successfully'},status=status.HTTP_200_OK)
    
    
    @action(methods=['GET'],detail=True,url_path="comments")
    def get_comment_byusername(self,request,pk=None):
        """
            this function will filter the data of the comments that has been created by the user by filtering the data from the Thread table foe better formatting ans understanding the comment very well  
        """
        try:
            test = Thread.objects.filter(post__comments__created_by__username = pk)
        except self.model.DoesNotExist as e:
            return Response({'info' : 'no such user exists !'})
        serializer = ThreadSerializer(test,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class CommentLikeDislikeView(ViewSet):
    serializer_class = CommentLikeDisLikeSerializer
    model = CommentLikeDislike
    queryset = CommentLikeDislike.objects.all()

    def list(self,request):
        serializer = self.serializer_class(self.queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    @action(methods=['POST'],detail=False,url_path="handle-like-dislike")
    def handle_vote_comment(self,request):
        user_id = request.data.get('user',None)
        comment_id = request.data.get('comment',None)
        vote = request.data.get('vote',None)

        comment = Comment.objects.get(pk=int(comment_id))
        commenter = Commenter.commenter.get(pk = int(user_id))

        user_vote,_ = self.model.objects.get_or_create(user=commenter,comment=comment)

        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            return Response(serializer.data,status=status.HTTP_200_OK)
        else: 
            if vote.lower() == user_vote.vote.lower():
    
                user_vote.delete()
                return Response({'info':'your vote has been delete success !'},status=status.HTTP_200_OK)
            else:
                user_vote.vote = vote.upper()
                user_vote.save()
            new_serializer = self.serializer_class(user_vote)
            return Response(new_serializer.data,status=status.HTTP_200_OK)
        