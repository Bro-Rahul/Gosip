from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager
from django.utils import timezone
from datetime import timedelta
import uuid
from django.core.mail import send_mail
# Create your models here.

class Role(models.TextChoices):
    ADMIN = 'AD','Admin'
    PUBLISHER = 'PB', 'Publisher',
    COMMENTER = 'CM', 'Commenter'

class PublisherManager(UserManager):
    def get_queryset(self,*args, **kwargs) -> models.QuerySet:
        return super().get_queryset(*args, **kwargs).filter(role=Role.PUBLISHER)
    
class CommenterManager(UserManager):
    def get_queryset(self,*args, **kwargs) -> models.QuerySet:
        return super().get_queryset(*args, **kwargs).filter(role=Role.COMMENTER)


class CustomeUserManager(UserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        print("inside the create_user method for saving ")
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('role', Role.PUBLISHER)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        email = self.normalize_email(email)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    avatar = models.ImageField(upload_to='profile/',null=True,blank=True)
    role = models.CharField(max_length=10,choices=Role.choices)
    base_role = Role.ADMIN

    objects = CustomeUserManager()
    publisher = PublisherManager()
    commenter = CommenterManager()
    
    def save(self,*args, **kwargs):
        if not self.pk:
            self.role = self.base_role
        return super().save(*args, **kwargs)
        
        
class Publisher(User):
    class Meta:
        proxy = True
    
    base_role = Role.PUBLISHER

    publisher = PublisherManager()
    

class Commenter(User):
    class Meta:
        proxy = True
    
    base_role = Role.COMMENTER

    commenter = CommenterManager()

class VerificationCode(models.Model):
    email = models.EmailField(unique=True)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now=True)

    def is_code_expired(self):
        return timezone.now() <= self.created_at + timedelta(minutes=10)
    
    def validate_code(self,typed_code):
        return self.is_code_expired() and typed_code == int(self.code)
     
    def __str__(self) -> str:
        return f"{self.code}  {self.email}"


class SecretKeys(models.Model):
    user = models.OneToOneField(Publisher,related_name="secret_key",on_delete=models.CASCADE)
    key = models.UUIDField(default=uuid.uuid4,null=True,blank=True)

    def save(self,*args, **kwargs):
        self.key = uuid.uuid4()
        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return f"the secret key of {self.user.username} is {self.key}"
    
class Followers(models.Model):
    user = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    followed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "followers"
        unique_together = ('user', 'follower')

    def __str__(self):
        return f"{self.follower} follows {self.user}"