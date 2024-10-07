from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    role = serializers.ReadOnlyField()

    profile = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id','username','password','role','email','profile']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
    def get_profile(self,obj):
        return obj.avatar.url if obj.avatar else None    

    def update(self, instance, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().update(instance, validated_data)

class PublisherSerializer(serializers.ModelSerializer):
    role = serializers.ReadOnlyField()
    class Meta:
        model = Publisher
        fields = ['id','username','password','role','email']

    def create(self, validated_data):
        return Publisher.objects.create_user(**validated_data)        


class CommenterSerializer(serializers.ModelSerializer):
    role = serializers.ReadOnlyField()
    class Meta:
        model = Commenter
        fields = ['id','username','password','email','role']

    def create(self, validated_data):
        return Commenter.objects.create_user(**validated_data)
        
class SecretKeySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset = Publisher.objects.all(),write_only=True)
    key = serializers.ReadOnlyField()
    class Meta: 
        model = SecretKeys
        fields = '__all__'

class VerificationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationCode
        exclude = ['created_at','code']