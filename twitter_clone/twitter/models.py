from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The email field cannot be empty")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('SuperUser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('SuperUser must have is_superuser=True')
        return self.create_user(email,password,**extra_fields)
    def get_by_natural_key(self, email):
        return self.get(email=email)

class AuthUser(AbstractBaseUser,PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255,unique=True)
    username = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    objects = UserManager()

#creating model for tweets and comments on posts
class Tweet(models.Model):
    title = models.TextField(max_length=200)
    tweet = models.TextField(max_length=2000)
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='tweets/images/', blank=True, null=True)
    def __str__(self):
        return self.tweet



#create user profile model
class Profile(models.Model):
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False, blank=True)
    
    date_modified = models.DateTimeField(AuthUser, auto_now=True)
    def __str__(self):
        return self.user.username


#create profiles when user signs up
#@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.set([instance.profile.id])
        user_profile.save()
post_save.connect(create_profile, sender=AuthUser)

class Follow(models.Model):
    following = models.ForeignKey(AuthUser, related_name='following', on_delete=models.CASCADE)
    follower = models.ForeignKey(AuthUser, related_name='followers', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
