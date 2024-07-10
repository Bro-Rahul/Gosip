from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from .permissions import *
from .models import *
from .serializer import *

# Create your views here.

class UserView(ViewSet):
    queryset = User.objects.all()
    model = User
    serializer_class = UserSerializer

    def list(self,request):
        serializer = UserSerializer(self.queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    @action(methods=['POST'],detail=False,url_path="create-commentor")
    def create_commenter(self,request):
        try:
            serializer = CommenterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as v:
            return Response({'info':v.message},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'info': 'something went wrong on the server side !'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(methods=['POST'],detail=False,url_path="create-publisher")
    def create_publisher(self,request):
        try:
            serializer = PublisherSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as v:
            return Response({'info':v.message},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'info': 'something went wrong on the server side !'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(methods=['PATCH'],detail=True,url_path="update-user")
    def update_user(self,request,pk=None):
        try:
            user = self.model.objects.get(pk=int(pk))

            serializer = self.serializer_class(instance=user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except self.model.DoesNotExist:
            return Response({'info': 'No such user account exists!'}, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk=None):
        try:
            user = self.model.objects.get(pk=int(pk))
        except self.model.DoesNotExist as e:
            return Response({'info' : 'no such user exists '},status=status.HTTP_400_BAD_REQUEST)
        
        user.delete()
        return Response({'info':'Account Has been delete !'},status=status.HTTP_200_OK)
        
class AuthenticationView(ObtainAuthToken):
    authentication_classes = [TokenAuthentication]
    def get_permissions(self):
        if self.request.method == 'DELETE':
            self.authentication_classes = [TokenAuthentication]
            self.permission_classes = [UserOrReadOnly]
        return super().get_permissions()
     
    def post(self, request, *args, **kwargs):
        username = request.data.get('username',None)
        email = request.data.get('email',None)
        commenter = Commenter.objects.filter(username = username,email = email).first()
        if not commenter:
            return Response({'info':'no such user exists with this creadencial'},status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            try:
                user = serializer.validated_data['user']
                user_instance = User.objects.get(username = user)
            except User.DoesNotExist as e:
                return Response({'info':'no such user exists !'},status=status.HTTP_400_BAD_REQUEST)
            
            token, created = Token.objects.get_or_create(user=user)
            data = {
                'token':token.key,
                'id' : commenter.pk,
                'profile' : commenter.avatar.url
            }
            return Response(data,status=status.HTTP_200_OK)
    
    def delete(self, request, pk=None):
        try:
            user = User.objects.get(pk = pk)
            self.check_object_permissions(request,user)
            user_token = Token.objects.get(user_id = pk)
        except Token.DoesNotExist as e:
            return Response({'info':'no such user token exists '},status=status.HTTP_400_BAD_REQUEST)    
        user_token.delete()
        return Response({'info' : 'Logout successfully !'},status=status.HTTP_200_OK)
    

class SecretKeyView(ViewSet):
    model = SecretKeys
    serializer_class = SecretKeySerializer

    @action(methods=['GET'],detail=True,url_path="get-secret-key")
    def get_secret_key(self,request,pk=None):
        user = Publisher.publisher.get(pk=int(pk))
        user_key , _ = self.model.objects.get_or_create(user=user)
        serializer = self.serializer_class(user_key)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    @action(methods=['GET'],detail=True,url_path="generate-new-secret-key")
    def generate_new_secret_key(self,request,pk=None):
        try:
            user = Publisher.publisher.get(pk=int(pk))
            oldKey = self.model.objects.get(user=user)        
            oldKey.save()
            serializer = self.serializer_class(oldKey)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Publisher.DoesNotExist as e:
            return Response({'info':'Publisher account is required ! '},status=status.HTTP_400_BAD_REQUEST)
        except:
            return self.get_secret_key(request,pk)
