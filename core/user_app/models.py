from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
# Create your models here.

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    image_profile = models.ImageField(null=True, blank=True,upload_to='users_profile_images')
    date_created = models.DateTimeField(auto_now_add = True, null=True, blank=True)


    def __str__(self):
        return self.user.first_name

