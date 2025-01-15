from django.db import models
from django.contrib.auth.models import User
import uuid

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True) 
    location = models.CharField(max_length=200, null=True, blank=True) 
    email = models.EmailField(max_length=500, null=True, blank=True)
    short_intro = models.CharField(max_length=1000, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    image_path = models.ImageField(null=True, blank=True, upload_to='profiles/' , default='profiles/user-default.png')
    social_github = models.CharField(max_length=500, null=True, blank=True)
    social_linkedin = models.CharField(max_length=500, null=True, blank=True)
    social_youtube = models.CharField(max_length=500, null=True, blank=True)
    social_website = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    def __str__(self):
        return str(self.username)
    
    class Meta:
        ordering = ['-username','-short_intro', '-location','-bio']
    
    @property
    def imageURL(self):
        try:
            url = self.image_path.url
        except:
            url = ''
        return url
        
    


class Skill(models.Model): 
    owner = models.ForeignKey(Profile,  on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    def __str__(self):
        return str(self.name)
    
class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    receiver = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages')
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
        
    def __str__(self):
        return str(self.subject)
    
    class Meta:
        ordering = ['is_read', '-created_at']