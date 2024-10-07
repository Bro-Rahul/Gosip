from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from .utils import send_mail_async
from .permissions import *
from .models import *
from .serializer import *
import random
import threading
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
                return Response({'info':'User created success !'},status=status.HTTP_200_OK)
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
        commenter = Commenter.commenter.get(username = username)
        if not commenter:
            return Response({'info':'no such user exists with this creadencial'},status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            try:
                user = serializer.validated_data['user']
            except User.DoesNotExist as e:
                return Response({'info':'no such user exists !'},status=status.HTTP_400_BAD_REQUEST)
            
            token, created = Token.objects.get_or_create(user=user)
            data = {
                'token':token.key,
                'id' : commenter.pk,
                'profile' : commenter.avatar.url if commenter.avatar else None
            }
            return Response(data,status=status.HTTP_200_OK)
    
    def delete(self, request, pk=None):
        try:
            user = User.objects.get(pk = pk)
            print(request.user)
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

class ValidateEmailCodeView(ViewSet):
    model = VerificationCode
    serializer_class = VerificationCodeSerializer

    @action(methods=['POST'],detail=False,url_path='verify-otp-code')
    def verify_emailcode(self,request):
        actual_data = self.model.objects.get(email = request.data['email'])
        if actual_data:
            result:bool = actual_data.validate_code(int(request.data['code']))
            if result == True:
                return Response(status=status.HTTP_200_OK)
            else:
                return Response({'info' : 'wrong otp enter !'},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'info' : 'no such user with this email exists'},status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['POST'],detail=False,url_path='generate-otp-code')
    def generate_code(self,request):
        new_verificationcode = random.choice(range(1000,9999))
        user_info ,created = self.model.objects.get_or_create(email = request.data)
        user_info.code = new_verificationcode
        user_info.save()

        email_str = render_to_string('email.html',{'verification_code' : new_verificationcode})
        threading.Thread(target=send_mail_async,args=(user_info.email,email_str)).start()
        return Response({'info': 'email is sended success!'},status=status.HTTP_200_OK)


class ForgetPasswordView(ViewSet):
    model = Commenter

    @action(methods=['GET'],detail = True,url_path="send-otp")
    def validate_user(self,request,pk=None):
        try:
            userinfo = self.model.objects.get(username = pk)
        except Exception as e:
            return Response({'info':'no such user exists '},status=status.HTTP_400_BAD_REQUEST)
        new_otp_code = random.choice(range(1000,9999))
        email_str = render_to_string('forgetPassword.html',{"user":userinfo,"otp":new_otp_code})
        user_otp =VerificationCode.objects.get(email = userinfo.email)
        user_otp.code = new_otp_code
        user_otp.save()
        threading.Thread(target=send_mail_async,args=(userinfo.email,email_str)).start()

        return Response({'info':'otp sended !'},status=status.HTTP_200_OK)
    
    @action(methods=['POST'],detail = False,url_path="verify-otp")
    def validate_otp(self,request):
        try:
            userinfo = self.model.objects.get(username = request.data['username'])
        except Exception as e:
            return Response({'info':'no such user exists '},status=status.HTTP_400_BAD_REQUEST)
        actual_otp = VerificationCode.objects.filter(email = userinfo.email).first()
        if actual_otp:
            result = actual_otp.validate_code(int(request.data['code']))
            if result == True:
                return Response({'info':'otp verified !'},status=status.HTTP_200_OK)
            else:
                return Response({'info':'enter an Valid otp !'},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'info':'otp does not verified !'},status=status.HTTP_400_BAD_REQUEST)
        
    @action(methods=['POST'],detail = False,url_path="change-password")
    def change_password(self,request):
        if not request.data.get('code',None):
            return Response({'info':'please verify with otp first '},status=status.HTTP_400_BAD_REQUEST)
        try:
            user_info = self.model.objects.get(username = request.data['username'])
            actual_otp = VerificationCode.objects.filter(email = user_info.email).first()
        except Exception as e:
            return Response({'info':'no such user exists '},status=status.HTTP_400_BAD_REQUEST)
        if actual_otp and actual_otp.validate_code(int(request.data['code'])):
            user_info.set_password(request.data['password'])
            user_info.save()
            return Response({'info':'pasword has been changed'},status = status.HTTP_200_OK)
        else:
            return Response({'info':'otp is not valid'},status=status.HTTP_400_BAD_REQUEST)
        
    